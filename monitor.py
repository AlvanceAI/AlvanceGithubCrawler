#!/usr/bin/env python3
"""Real-time TUI monitor for the AlvanceGithubCrawler pipeline."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

try:
    from rich.console import Console
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich", "-q"], check=True)
    from rich.console import Console
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text

STATE_DIR = Path(sys.argv[1]) / ".crawler-state" if len(sys.argv) > 1 else Path(".crawler-state")
CANDIDATES = STATE_DIR / "candidates.jsonl"
PENDING = STATE_DIR / "pending.jsonl"
REJECTIONS = STATE_DIR / "rejections.jsonl"


def read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return records


def pipeline_process() -> tuple[int, str]:
    result = subprocess.run(
        ["pgrep", "-a", "-f", "alvance-github-crawler"],
        capture_output=True, text=True
    )
    lines = [l for l in result.stdout.splitlines() if "monitor" not in l]
    if lines:
        pid = lines[0].split()[0]
        cmd = " ".join(lines[0].split()[2:])
        return int(pid), cmd
    return 0, ""


def pending_stats(records: list[dict]) -> dict:
    active: dict[str, dict] = {}
    attempts: Counter = Counter()
    for r in records:
        key = str(r.get("key") or "")
        event = str(r.get("event") or "")
        if not key:
            continue
        if event in {"queued", "requeued"} and isinstance(r.get("candidate"), dict):
            active[key] = r["candidate"]
        elif event == "deferred":
            item = active.pop(key, None)
            if item is not None:
                active[key] = item
        elif event == "completed":
            active.pop(key, None)
        elif event == "attempted":
            attempts[key] += 1
    return {"active": len(active), "attempts": dict(attempts)}


def rejection_summary(records: list[dict]) -> Counter:
    latest: dict[str, str] = {}
    for r in records:
        repo = str(r.get("repo") or "")
        reason = str(r.get("reason") or "")
        if repo:
            latest[repo] = reason
    return Counter(latest.values())


def candidate_summary(records: list[dict]) -> Counter:
    seen: set[str] = set()
    langs: Counter = Counter()
    for r in records:
        repo = str(r.get("repo") or "")
        if repo and repo not in seen:
            seen.add(repo)
            lang = str(r.get("language") or "unknown").lower()
            langs[lang] += 1
    return langs


def build_layout(console: Console) -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3),
    )
    layout["body"].split_row(
        Layout(name="left"),
        Layout(name="right"),
    )
    return layout


def render(layout: Layout) -> None:
    pid, cmd = pipeline_process()
    candidates = read_jsonl(CANDIDATES)
    pending_records = read_jsonl(PENDING)
    rejections = read_jsonl(REJECTIONS)

    pstats = pending_stats(pending_records)
    rstats = rejection_summary(rejections)
    cstats = candidate_summary(candidates)

    # Header
    status = Text()
    if pid:
        status.append("● RUNNING ", style="bold green")
        status.append(f"PID {pid}  ", style="dim")
        status.append(cmd[-80:], style="dim cyan")
    else:
        status.append("○ IDLE", style="bold yellow")
    layout["header"].update(Panel(status, title="[bold]Alvance Pipeline Monitor[/bold]"))

    # Left: candidates
    ctable = Table(show_header=True, header_style="bold magenta", box=None, padding=(0, 1))
    ctable.add_column("Language", style="cyan")
    ctable.add_column("Count", justify="right", style="green")
    total = sum(cstats.values())
    for lang, count in sorted(cstats.items(), key=lambda x: -x[1]):
        ctable.add_row(lang, str(count))
    ctable.add_row("─" * 12, "─" * 5)
    ctable.add_row("[bold]Total[/bold]", f"[bold]{total}[/bold]")

    layout["left"].update(Panel(
        ctable,
        title=f"[bold green]✓ Candidates ({total})[/bold green]",
    ))

    # Right: pending + rejections
    rtable = Table(show_header=True, header_style="bold yellow", box=None, padding=(0, 1))
    rtable.add_column("Reason", style="yellow")
    rtable.add_column("Count", justify="right")
    for reason, count in sorted(rstats.items(), key=lambda x: -x[1])[:12]:
        color = "red" if "fail" in reason or "error" in reason else "yellow"
        rtable.add_row(f"[{color}]{reason}[/{color}]", str(count))

    pending_text = Text()
    pending_text.append(f"Active pending: ", style="bold")
    pending_text.append(f"{pstats['active']}\n", style="bold cyan")
    pending_text.append(f"Total rejections: ", style="bold")
    pending_text.append(f"{len(rejections)}\n\n", style="bold red")
    pending_text.append_text(Text.from_markup("[bold]Rejection breakdown:[/bold]\n"))

    from rich.console import Group
    layout["right"].update(Panel(
        Group(pending_text, rtable),
        title="[bold yellow]Queue & Rejections[/bold yellow]",
    ))

    # Footer
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    layout["footer"].update(Panel(
        Text(f"Last updated: {ts}  |  Press Ctrl+C to exit", style="dim"),
    ))


def main() -> None:
    console = Console()
    layout = build_layout(console)
    with Live(layout, console=console, refresh_per_second=0.5, screen=True):
        try:
            while True:
                render(layout)
                time.sleep(2)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
