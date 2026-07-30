#!/usr/bin/env python3
"""Launch and monitor the resumable Alvance production pipeline."""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import signal
import subprocess
import time
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from alvance_github_crawler.config import PipelineConfig

REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_STATE_DIR = Path(
    os.environ.get("PIPELINE_OUTPUT_DIR", "outputs/github_production_500_unquota")
)
DEFAULT_CRAWL_DIR = Path(
    os.environ.get("CRAWL_OUTPUT_DIR", "outputs/github_crawl_500_unquota")
)
DEFAULT_RUN_ROOT = Path(
    os.environ.get("PIPELINE_RUN_ROOT", "outputs/production-runs")
)
LANGUAGE_ORDER = ("python", "go", "typescript", "javascript", "rust")
SAFE_RUN_ID = re.compile(r"^[A-Za-z0-9._-]+$")
STAGE_PRIORITY = {
    "E2B verify": 0,
    "Prescreen": 1,
    "GitHub crawl": 2,
    "Driver": 3,
}


@dataclass(frozen=True)
class PipelineProcess:
    pid: int
    stage: str
    command: str


@dataclass
class ManagedPipeline:
    process: subprocess.Popen[bytes]
    log_handle: Any
    log_path: Path
    ceiling_per_language: int

    def close_log(self) -> None:
        if not self.log_handle.closed:
            self.log_handle.close()


def resolve_path(path: Path) -> Path:
    path = path.expanduser()
    return path if path.is_absolute() else REPO_ROOT / path


def configured_e2b_key_count() -> int:
    """Read the configured numbered E2B slots without exposing their values."""
    try:
        return len(PipelineConfig.from_env().e2b_api_keys)
    except (OSError, ValueError):
        return 0


def configured_github_token_count() -> int:
    """Read the configured GitHub token pool size without exposing values."""
    try:
        return len(PipelineConfig.from_env().github_tokens)
    except (OSError, ValueError):
        return 0


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return records
    for line in text.splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            records.append(value)
    return records


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def line_count(path: Path) -> int:
    if not path.is_file():
        return 0
    try:
        with path.open("rb") as handle:
            return sum(1 for _ in handle)
    except OSError:
        return 0


def _process_stage(arguments: list[str]) -> str:
    if "--verify-pending" in arguments:
        return "E2B verify"
    if "produce" in arguments and any("alvance-github-crawler" in arg for arg in arguments):
        return "Prescreen"
    if "crawl" in arguments and any("alvance-github-crawler" in arg for arg in arguments):
        return "GitHub crawl"
    if any(Path(arg).name in {"run_continuous_production.sh", "run.sh"} for arg in arguments):
        return "Driver"
    return ""


def pipeline_processes() -> list[PipelineProcess]:
    """Return one leaf-most process per active pipeline stage."""
    by_stage: dict[str, PipelineProcess] = {}
    proc_root = Path("/proc")
    if not proc_root.is_dir():
        return []
    for entry in proc_root.iterdir():
        if not entry.name.isdigit() or int(entry.name) == os.getpid():
            continue
        try:
            raw_arguments = (entry / "cmdline").read_bytes().split(b"\0")
        except (OSError, PermissionError):
            continue
        arguments = [part.decode(errors="replace") for part in raw_arguments if part]
        if not arguments or any(Path(arg).name == "monitor.py" for arg in arguments):
            continue
        stage = _process_stage(arguments)
        if not stage:
            continue
        pid = int(entry.name)
        process = PipelineProcess(pid=pid, stage=stage, command=shlex.join(arguments))
        previous = by_stage.get(stage)
        if previous is None or pid > previous.pid:
            by_stage[stage] = process
    return sorted(by_stage.values(), key=lambda process: STAGE_PRIORITY[process.stage])


def build_pipeline_environment(
    args: argparse.Namespace,
    *,
    ceiling_per_language: int,
) -> dict[str, str]:
    environment = os.environ.copy()
    environment.update(
        {
            "PIPELINE_RUN_ID": args.run_id,
            "PIPELINE_RUN_ROOT": str(args.run_root),
            "CRAWL_OUTPUT_DIR": str(args.crawl_dir),
            "PRODUCTION_OUTPUT_DIR": str(args.state_dir),
            "PUBLISH_BRANCH": args.publish_branch,
            "MAX_PER_LANGUAGE": str(ceiling_per_language),
            "BATCH_PER_LANGUAGE": str(args.batch_per_language),
            "PRESCREEN_CONCURRENCY": str(args.prescreen_concurrency),
            "E2B_CONCURRENCY": str(args.e2b_concurrency),
            "PUBLISH_TASKS": "true",
            "PUBLISH_RUN_ARTIFACTS": "true",
        }
    )
    return environment


def launch_pipeline(
    args: argparse.Namespace,
    *,
    ceiling_per_language: int,
) -> ManagedPipeline:
    run_dir = args.run_root / args.run_id
    log_dir = run_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "launcher.log"
    log_handle = log_path.open("ab", buffering=0)
    timestamp = datetime.now(UTC).isoformat()
    banner = (
        f"\n[{timestamp}] monitor launch max_per_language={ceiling_per_language} "
        f"batch_per_language={args.batch_per_language} "
        f"prescreen_concurrency={args.prescreen_concurrency} "
        f"e2b_concurrency_per_key={args.e2b_concurrency}\n"
    )
    log_handle.write(banner.encode())
    try:
        process = subprocess.Popen(
            ["bash", str(REPO_ROOT / "scripts/run_continuous_production.sh")],
            cwd=REPO_ROOT,
            env=build_pipeline_environment(
                args,
                ceiling_per_language=ceiling_per_language,
            ),
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    except Exception:
        log_handle.close()
        raise
    return ManagedPipeline(
        process=process,
        log_handle=log_handle,
        log_path=log_path,
        ceiling_per_language=ceiling_per_language,
    )


def stop_pipeline(pipeline: ManagedPipeline) -> int:
    if pipeline.process.poll() is not None:
        return int(pipeline.process.returncode or 0)
    for sig, timeout in ((signal.SIGINT, 10), (signal.SIGTERM, 15)):
        try:
            os.killpg(pipeline.process.pid, sig)
        except ProcessLookupError:
            break
        try:
            return pipeline.process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            continue
    try:
        os.killpg(pipeline.process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    return pipeline.process.wait()


def pending_stats(records: list[dict[str, Any]]) -> dict[str, Any]:
    active: dict[str, dict[str, Any]] = {}
    attempts: Counter[str] = Counter()
    for record in records:
        key = str(record.get("key") or "")
        event = str(record.get("event") or "")
        if not key:
            continue
        if event in {"queued", "requeued"}:
            candidate = record.get("candidate")
            active[key] = candidate if isinstance(candidate, dict) else {}
        elif event == "completed":
            active.pop(key, None)
        elif event == "attempted":
            attempts[key] += 1
    return {"active": len(active), "attempts": dict(attempts)}


def rejection_summary(records: list[dict[str, Any]]) -> Counter[str]:
    latest: dict[str, str] = {}
    for record in records:
        repo = str(record.get("repo") or "")
        reason = str(record.get("reason") or "unknown")
        if repo:
            latest[repo] = reason
    return Counter(latest.values())


def _candidate_identity(record: dict[str, Any], index: int) -> str:
    package = record.get("harbor_package")
    task_path = str(package.get("task_path") or "") if isinstance(package, dict) else ""
    repo = str(record.get("repo") or "")
    base_commit = str(record.get("base_commit") or "")
    return task_path or (f"{repo}@{base_commit}" if repo else f"row:{index}")


def candidate_summary(records: list[dict[str, Any]]) -> Counter[str]:
    seen: set[str] = set()
    languages: Counter[str] = Counter()
    for index, record in enumerate(records):
        identity = _candidate_identity(record, index)
        if identity in seen:
            continue
        seen.add(identity)
        languages[str(record.get("language") or "unknown").lower()] += 1
    return languages


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = f"{normalized[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def task_rate_summary(
    records: list[dict[str, Any]],
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Estimate completed Task throughput from unique registry records.

    Rates are extrapolated from the number of unique Tasks registered in the
    trailing 15-minute and 60-minute windows. Invalid or missing timestamps do
    not affect the estimate.
    """
    current = now or datetime.now(UTC)
    if current.tzinfo is None:
        current = current.replace(tzinfo=UTC)
    current = current.astimezone(UTC)

    seen: set[str] = set()
    timestamps: list[datetime] = []
    for index, record in enumerate(records):
        identity = _candidate_identity(record, index)
        if identity in seen:
            continue
        seen.add(identity)
        registered_at = _parse_timestamp(record.get("registered_at"))
        if registered_at is not None:
            timestamps.append(registered_at)

    def window_stats(window: timedelta) -> tuple[int, float]:
        cutoff = current - window
        count = sum(cutoff <= timestamp <= current for timestamp in timestamps)
        return count, count * 3600.0 / window.total_seconds()

    count_15m, rate_15m = window_stats(timedelta(minutes=15))
    count_60m, rate_60m = window_stats(timedelta(hours=1))
    latest = max(timestamps, default=None)
    return {
        "last_15m_count": count_15m,
        "last_15m_per_hour": rate_15m,
        "last_60m_count": count_60m,
        "last_60m_per_hour": rate_60m,
        "latest_at": latest,
    }


def latest_run_dir(run_root: Path) -> Path | None:
    try:
        directories = [path for path in run_root.iterdir() if path.is_dir()]
    except OSError:
        return None
    return max(directories, key=lambda path: path.stat().st_mtime, default=None)


def build_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3),
    )
    layout["body"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=1),
    )
    return layout


def _ordered_languages(stats: Counter[str]) -> list[tuple[str, int]]:
    known = [(language, stats[language]) for language in LANGUAGE_ORDER if stats[language]]
    extras = sorted(
        ((language, count) for language, count in stats.items() if language not in LANGUAGE_ORDER),
        key=lambda item: (-item[1], item[0]),
    )
    return known + extras


def render(
    layout: Layout,
    *,
    state_dir: Path,
    crawl_dir: Path,
    run_root: Path,
    terminal_status: tuple[str, str] | None = None,
    launcher_pid: int | None = None,
    footer_hint: str = "Press Ctrl+C to exit",
    ceiling_per_language: int | None = None,
    prescreen_concurrency: int | None = None,
    e2b_concurrency_per_key: int | None = None,
    e2b_key_count: int = 0,
    github_token_count: int = 0,
) -> None:
    candidates = read_jsonl(state_dir / "candidates.jsonl")
    pending_records = read_jsonl(state_dir / "pending.jsonl")
    rejections = read_jsonl(state_dir / "rejections.jsonl")
    pstats = pending_stats(pending_records)
    rstats = rejection_summary(rejections)
    cstats = candidate_summary(candidates)
    rate = task_rate_summary(candidates)
    processes = pipeline_processes()

    raw_total = line_count(crawl_dir / "raw_repositories.jsonl")
    accepted_total = line_count(crawl_dir / "accepted_repositories.jsonl")
    crawl_state = read_json(crawl_dir / "crawl_state.json")
    target_total = int(crawl_state.get("target_total") or raw_total)
    completion = (100.0 * raw_total / target_total) if target_total else 0.0

    run_dir = latest_run_dir(run_root)
    timings = read_jsonl(run_dir / "stage-timings.jsonl") if run_dir else []
    last_stage = timings[-1] if timings else {}

    status = Text(overflow="ellipsis", no_wrap=True)
    if terminal_status:
        label, style = terminal_status
        status.append(label, style=style)
    elif processes:
        status.append("● RUNNING  ", style="bold green")
        status.append(
            " | ".join(f"{process.stage} PID {process.pid}" for process in processes),
            style="bold cyan",
        )
        status.append(f"  {processes[0].command}", style="dim cyan")
    elif launcher_pid:
        status.append("● STARTING  ", style="bold green")
        status.append(f"driver PID {launcher_pid}", style="bold cyan")
    elif pstats["active"]:
        status.append("■ PAUSED  ", style="bold yellow")
        status.append(f"{pstats['active']} pending tasks preserved", style="yellow")
    else:
        status.append("○ IDLE", style="bold yellow")
    layout["header"].update(Panel(status, title="[bold]Alvance Pipeline Monitor[/bold]"))

    candidate_table = Table(
        show_header=True,
        header_style="bold magenta",
        box=None,
        padding=(0, 1),
        expand=False,
    )
    candidate_table.add_column("Language", style="cyan")
    candidate_table.add_column("Count", justify="right", style="green")
    deliverable_total = sum(cstats.values())
    for language, count in _ordered_languages(cstats):
        candidate_table.add_row(language, str(count))
    if not cstats:
        candidate_table.add_row("none", "0", style="dim")
    candidate_table.add_row("─" * 12, "─" * 7)
    candidate_table.add_row("[bold]Total[/bold]", f"[bold]{deliverable_total}[/bold]")
    layout["left"].update(
        Panel(
            candidate_table,
            title=f"[bold green]✓ Deliverable Tasks ({deliverable_total})[/bold green]",
        )
    )

    rejection_table = Table(
        show_header=True,
        header_style="bold yellow",
        box=None,
        padding=(0, 1),
        expand=False,
    )
    rejection_table.add_column("Reason", style="yellow")
    rejection_table.add_column("Count", justify="right")
    for reason, count in rstats.most_common(12):
        color = "red" if "fail" in reason or "error" in reason else "yellow"
        rejection_table.add_row(f"[{color}]{reason}[/{color}]", str(count))

    summary = Text()
    summary.append("Raw repositories: ", style="bold")
    summary.append(f"{raw_total:,} / {target_total:,} ({completion:.1f}%)\n", style="cyan")
    summary.append("Initial filter accepted: ", style="bold")
    summary.append(f"{accepted_total:,}\n", style="green")
    if ceiling_per_language:
        summary.append("Current crawl ceiling: ", style="bold")
        summary.append(f"{ceiling_per_language * len(LANGUAGE_ORDER):,}\n", style="cyan")
    if github_token_count:
        summary.append("GitHub token pool: ", style="bold")
        summary.append(f"{github_token_count}\n", style="bold cyan")
    if prescreen_concurrency:
        summary.append("Prescreen workers: ", style="bold")
        summary.append(f"{prescreen_concurrency}\n", style="cyan")
    if e2b_concurrency_per_key:
        total_e2b_workers = e2b_concurrency_per_key * e2b_key_count
        summary.append("E2B workers: ", style="bold")
        summary.append(
            f"{e2b_concurrency_per_key}/key x {e2b_key_count} = {total_e2b_workers}\n",
            style="bold cyan",
        )
    summary.append("Task rate (rolling): ", style="bold")
    summary.append(
        f"{rate['last_15m_per_hour']:.1f}/h (15m) | "
        f"{rate['last_60m_per_hour']:.1f}/h (60m)\n",
        style="bold green",
    )
    if rate["latest_at"] is not None:
        latest_local = rate["latest_at"].astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
        summary.append("Latest Task: ", style="bold")
        summary.append(f"{latest_local}\n", style="dim")
    summary.append("Active pending: ", style="bold")
    summary.append(f"{pstats['active']:,}\n", style="bold cyan")
    summary.append("Rejected repositories: ", style="bold")
    summary.append(f"{sum(rstats.values()):,}", style="bold red")
    summary.append(f"  ({len(rejections):,} events)\n", style="dim")
    if last_stage:
        summary.append("Last stage: ", style="bold")
        summary.append(str(last_stage.get("stage") or "unknown"), style="magenta")
        summary.append(
            f"  exit={last_stage.get('exit_code', '?')}  "
            f"duration={last_stage.get('duration_s', 0)}s\n",
            style="dim",
        )
    summary.append("\nRejection breakdown:\n", style="bold")
    layout["right"].update(
        Panel(
            Group(summary, rejection_table),
            title="[bold yellow]Queue & Rejections[/bold yellow]",
        )
    )

    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    source = state_dir.relative_to(REPO_ROOT) if state_dir.is_relative_to(REPO_ROOT) else state_dir
    footer = Text(
        f"Last updated: {timestamp}  |  Source: {source}  |  {footer_hint}",
        style="dim",
        overflow="ellipsis",
        no_wrap=True,
    )
    layout["footer"].update(Panel(footer))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "state_dir",
        nargs="?",
        type=Path,
        default=DEFAULT_STATE_DIR,
        help="production state directory containing candidates/pending/rejections JSONL",
    )
    parser.add_argument("--crawl-dir", type=Path, default=DEFAULT_CRAWL_DIR)
    parser.add_argument("--run-root", type=Path, default=DEFAULT_RUN_ROOT)
    parser.add_argument("--interval", type=float, default=2.0, help="refresh interval in seconds")
    parser.add_argument(
        "--monitor-only",
        action="store_true",
        help="show the dashboard without starting or resuming production",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="render one read-only snapshot and exit (implies --monitor-only)",
    )
    parser.add_argument(
        "--no-alt-screen",
        action="store_true",
        help="refresh in the current terminal buffer instead of the alternate screen",
    )
    parser.add_argument(
        "--run-id",
        default=os.environ.get("PIPELINE_RUN_ID")
        or f"github-mass-production-XBY-{datetime.now(UTC):%Y%m%d}",
    )
    parser.add_argument(
        "--publish-branch",
        default=os.environ.get("PUBLISH_BRANCH", "XBY"),
    )
    parser.add_argument(
        "--max-per-language",
        type=int,
        default=int(os.environ.get("MAX_PER_LANGUAGE", "2000")),
        help="initial per-language crawl ceiling (default: 2000, or 10000 total)",
    )
    parser.add_argument(
        "--extension-per-language",
        type=int,
        default=1000,
        help="increase after a complete cycle while E2B keys still have capacity",
    )
    parser.add_argument(
        "--stop-at-max",
        action="store_true",
        help="stop at --max-per-language instead of extending until keys are exhausted",
    )
    parser.add_argument(
        "--batch-per-language",
        type=int,
        default=int(os.environ.get("BATCH_PER_LANGUAGE", "100")),
    )
    parser.add_argument(
        "--prescreen-concurrency",
        type=int,
        default=int(os.environ.get("PRESCREEN_CONCURRENCY", "20")),
    )
    parser.add_argument(
        "--e2b-concurrency",
        type=int,
        default=int(os.environ.get("E2B_CONCURRENCY", "20")),
        help="concurrency per E2B key; each numbered key provides this value",
    )
    args = parser.parse_args(argv)
    if args.interval <= 0:
        parser.error("--interval must be greater than zero")
    if args.max_per_language < 1 or args.extension_per_language < 1:
        parser.error("crawl ceilings must be positive")
    if args.batch_per_language < 1:
        parser.error("--batch-per-language must be positive")
    if not 1 <= args.prescreen_concurrency <= 20:
        parser.error("--prescreen-concurrency must be between 1 and 20")
    if not 1 <= args.e2b_concurrency <= 20:
        parser.error("--e2b-concurrency must be between 1 and 20 per key")
    if not SAFE_RUN_ID.fullmatch(args.run_id):
        parser.error("--run-id may contain only letters, digits, dot, underscore, and hyphen")
    args.state_dir = resolve_path(args.state_dir)
    args.crawl_dir = resolve_path(args.crawl_dir)
    args.run_root = resolve_path(args.run_root)
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    e2b_key_count = configured_e2b_key_count()
    github_token_count = configured_github_token_count()
    console = Console()
    layout = build_layout()
    if args.once:
        render(
            layout,
            state_dir=args.state_dir,
            crawl_dir=args.crawl_dir,
            run_root=args.run_root,
            e2b_key_count=e2b_key_count,
            github_token_count=github_token_count,
        )
        console.print(layout)
        return 0

    managed: ManagedPipeline | None = None
    attached = False
    ceiling_per_language = args.max_per_language
    if not args.monitor_only:
        active_processes = pipeline_processes()
        if active_processes:
            attached = True
        else:
            try:
                managed = launch_pipeline(
                    args,
                    ceiling_per_language=ceiling_per_language,
                )
            except OSError as exc:
                console.print(f"[bold red]Unable to start pipeline:[/bold red] {exc}")
                return 2

    refresh_per_second = max(1.0, min(10.0, 1.0 / args.interval))
    terminal_status: tuple[str, str] | None = None
    final_code = 0
    footer_hint = (
        "Press Ctrl+C to pause pipeline and exit"
        if managed
        else "Press Ctrl+C to exit"
    )
    with Live(
        layout,
        console=console,
        refresh_per_second=refresh_per_second,
        screen=console.is_terminal and not args.no_alt_screen,
    ):
        try:
            while True:
                if managed and managed.process.poll() is not None:
                    final_code = int(managed.process.returncode or 0)
                    managed.close_log()
                    exhausted = (args.run_root / args.run_id / "e2b-keys-exhausted").is_file()
                    if final_code == 0 and not args.stop_at_max and not exhausted:
                        ceiling_per_language += args.extension_per_language
                        managed = launch_pipeline(
                            args,
                            ceiling_per_language=ceiling_per_language,
                        )
                        footer_hint = "Press Ctrl+C to pause pipeline and exit"
                    else:
                        if exhausted or final_code == 4:
                            terminal_status = ("◆ E2B KEYS EXHAUSTED", "bold yellow")
                            final_code = 0
                        elif final_code == 0:
                            terminal_status = ("✓ PIPELINE COMPLETE", "bold green")
                        else:
                            terminal_status = (
                                f"× PIPELINE STOPPED  exit={final_code}",
                                "bold red",
                            )
                        footer_hint = f"Pipeline finished; log: {managed.log_path}"

                if attached and not pipeline_processes():
                    terminal_status = ("■ ATTACHED PIPELINE STOPPED", "bold yellow")
                    footer_hint = "Attached pipeline stopped; press Ctrl+C to exit"

                render(
                    layout,
                    state_dir=args.state_dir,
                    crawl_dir=args.crawl_dir,
                    run_root=args.run_root,
                    terminal_status=terminal_status,
                    launcher_pid=(
                        managed.process.pid
                        if managed and managed.process.poll() is None
                        else None
                    ),
                    footer_hint=footer_hint,
                    ceiling_per_language=(
                        ceiling_per_language if not args.monitor_only else None
                    ),
                    prescreen_concurrency=(
                        args.prescreen_concurrency if not args.monitor_only else None
                    ),
                    e2b_concurrency_per_key=(
                        args.e2b_concurrency if not args.monitor_only else None
                    ),
                    e2b_key_count=e2b_key_count,
                    github_token_count=github_token_count,
                )
                if terminal_status:
                    time.sleep(3)
                    break
                time.sleep(args.interval)
        except KeyboardInterrupt:
            if managed and managed.process.poll() is None:
                terminal_status = ("■ PAUSING PIPELINE", "bold yellow")
                render(
                    layout,
                    state_dir=args.state_dir,
                    crawl_dir=args.crawl_dir,
                    run_root=args.run_root,
                    terminal_status=terminal_status,
                    footer_hint="Waiting for checkpoint-safe shutdown",
                    ceiling_per_language=ceiling_per_language,
                    prescreen_concurrency=args.prescreen_concurrency,
                    e2b_concurrency_per_key=args.e2b_concurrency,
                    e2b_key_count=e2b_key_count,
                    github_token_count=github_token_count,
                )
                final_code = stop_pipeline(managed)
                terminal_status = ("■ PIPELINE PAUSED", "bold yellow")
            else:
                terminal_status = ("■ MONITOR CLOSED", "bold yellow")
            render(
                layout,
                state_dir=args.state_dir,
                crawl_dir=args.crawl_dir,
                run_root=args.run_root,
                terminal_status=terminal_status,
                footer_hint="Checkpoint and logs preserved",
                ceiling_per_language=(ceiling_per_language if managed else None),
                prescreen_concurrency=(args.prescreen_concurrency if managed else None),
                e2b_concurrency_per_key=(args.e2b_concurrency if managed else None),
                e2b_key_count=e2b_key_count,
                github_token_count=github_token_count,
            )
        finally:
            if managed:
                managed.close_log()

    console.print(layout)
    return final_code if final_code not in {130, 143, -signal.SIGINT, -signal.SIGTERM} else 0


if __name__ == "__main__":
    raise SystemExit(main())
