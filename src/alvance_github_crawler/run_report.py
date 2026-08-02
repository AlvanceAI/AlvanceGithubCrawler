from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .jsonl_io import read_text_locked, split_jsonl_lines


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in split_jsonl_lines(read_text_locked(path)):
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows


def pending_count(path: Path) -> int:
    active: set[str] = set()
    for event in read_jsonl(path):
        key = str(event.get("key") or "")
        if not key:
            continue
        if event.get("event") in {"queued", "requeued"}:
            active.add(key)
        elif event.get("event") == "completed":
            active.discard(key)
    return len(active)


def build_summary(
    *,
    run_id: str,
    crawl_dir: Path,
    production_dir: Path,
    timings_path: Path,
) -> dict[str, Any]:
    crawl = _read_json(crawl_dir / "summary.json")
    candidates = read_jsonl(production_dir / "candidates.jsonl")
    rejections = read_jsonl(production_dir / "rejections.jsonl")
    pending_events = read_jsonl(production_dir / "pending.jsonl")
    timings = read_jsonl(timings_path)
    latest_rejections = {
        str(record.get("repo") or ""): record
        for record in rejections
        if record.get("repo")
    }
    queued_keys = {
        str(event.get("key"))
        for event in pending_events
        if event.get("event") == "queued" and event.get("key")
    }
    candidate_languages = Counter(str(row.get("language") or "unknown") for row in candidates)
    resource_tiers = Counter(
        (
            int((row.get("e2b_environment") or {}).get("cpu_count") or 1),
            int((row.get("e2b_environment") or {}).get("memory_mb") or 1_024),
        )
        for row in candidates
    )
    rejection_reasons = Counter(
        str(record.get("reason") or "unknown") for record in latest_rejections.values()
    )
    remaining = pending_count(production_dir / "pending.jsonl")
    crawl_complete = crawl.get("completed") is True or crawl.get("status") == "completed"
    return {
        "schema_version": "1.0",
        "run_id": run_id,
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "complete" if crawl_complete and remaining == 0 else "incomplete",
        "paths": {
            "crawl_dir": str(crawl_dir),
            "production_dir": str(production_dir),
            "timings": str(timings_path),
        },
        "crawl": crawl,
        "production": {
            "e2b_queued_total": len(queued_keys),
            "pending_remaining": remaining,
            "candidate_total": len(candidates),
            "candidate_by_language": dict(sorted(candidate_languages.items())),
            "candidate_by_resource": {
                f"{cpu}cpu-{memory}mb": count
                for (cpu, memory), count in sorted(resource_tiers.items())
            },
            "rejection_record_total": len(rejections),
            "latest_rejection_total": len(latest_rejections),
            "latest_rejection_by_reason": dict(rejection_reasons.most_common()),
        },
        "stage_timings": timings,
        "candidates": [_candidate_metrics(row) for row in candidates],
    }


def render_markdown(summary: dict[str, Any]) -> str:
    crawl = summary.get("crawl") or {}
    production = summary.get("production") or {}
    lines = [
        f"# Pipeline statistics: {summary['run_id']}",
        "",
        f"- Status: `{summary['status']}`",
        f"- Generated: `{summary['generated_at']}`",
        f"- Raw GitHub sample: {crawl.get('fetched_total', 0)}",
        f"- Initial filter accepted: {crawl.get('accepted_total', 0)}",
        f"- E2B queue: {production.get('e2b_queued_total', 0)}",
        f"- Deliverable tasks: {production.get('candidate_total', 0)}",
        f"- Pending: {production.get('pending_remaining', 0)}",
        "",
        "## Language funnel",
        "",
        "| Language | Initial accepted | Final tasks |",
        "|---|---:|---:|",
    ]
    accepted = crawl.get("accepted_by_language") or {}
    final = production.get("candidate_by_language") or {}
    for language in ("python", "go", "typescript", "javascript", "rust"):
        lines.append(f"| {language} | {accepted.get(language, 0)} | {final.get(language, 0)} |")
    lines.extend(
        [
            "",
            "## Stage timings",
            "",
            "| Stage | Duration (s) | Exit |",
            "|---|---:|---:|",
        ]
    )
    for timing in summary.get("stage_timings") or []:
        lines.append(
            f"| {timing.get('stage', '')} | {timing.get('duration_s', 0)} | "
            f"{timing.get('exit_code', '')} |"
        )
    lines.extend(
        [
            "",
            "## E2B task performance",
            "",
            "| Repository | Language | Resources | Cold start (s) | Tests (s) | Peak MB | Task |",
            "|---|---|---|---:|---:|---:|---|",
        ]
    )
    for candidate in summary.get("candidates") or []:
        lines.append(
            f"| [{candidate['repo']}](https://github.com/{candidate['repo']}) | "
            f"{candidate['language']} | {candidate['cpu_count']} CPU / "
            f"{candidate['memory_mb']} MB | {candidate['cold_start_median_s']} | "
            f"{candidate['test_duration_median_s']} | {candidate['peak_mem_median_mb']} | "
            f"`{candidate['task_path']}` |"
        )
    lines.extend(
        [
            "",
            "## Logs",
            "",
            f"Raw stage logs are under `{Path(summary['paths']['timings']).parent / 'logs'}`.",
            "",
        ]
    )
    return "\n".join(lines)


def _candidate_metrics(row: dict[str, Any]) -> dict[str, Any]:
    environment = row.get("e2b_environment") or {}
    benchmark = row.get("benchmark") or {}
    package = row.get("harbor_package") or {}
    return {
        "repo": str(row.get("repo") or ""),
        "language": str(row.get("language") or ""),
        "base_commit": str(row.get("base_commit") or ""),
        "status": str(row.get("status") or ""),
        "cpu_count": int(environment.get("cpu_count") or 1),
        "memory_mb": int(environment.get("memory_mb") or 1_024),
        "cold_start_median_s": benchmark.get("cold_start_median_s"),
        "test_duration_median_s": benchmark.get("test_duration_median_s"),
        "peak_mem_median_mb": benchmark.get("peak_mem_median_mb"),
        "offline_duration_s": (environment.get("offline") or {}).get("duration_s"),
        "task_path": str(package.get("task_path") or ""),
        "launch_command": str(package.get("launch_command") or ""),
    }


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    pending_parser = subparsers.add_parser("pending-count")
    pending_parser.add_argument("path", type=Path)
    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--run-id", required=True)
    build_parser.add_argument("--crawl-dir", required=True, type=Path)
    build_parser.add_argument("--production-dir", required=True, type=Path)
    build_parser.add_argument("--timings", required=True, type=Path)
    build_parser.add_argument("--output-json", required=True, type=Path)
    build_parser.add_argument("--output-md", required=True, type=Path)
    args = parser.parse_args(argv)

    if args.command == "pending-count":
        print(pending_count(args.path))
        return 0

    summary = build_summary(
        run_id=args.run_id,
        crawl_dir=args.crawl_dir,
        production_dir=args.production_dir,
        timings_path=args.timings,
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    args.output_md.write_text(render_markdown(summary), encoding="utf-8")
    print(args.output_json)
    print(args.output_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
