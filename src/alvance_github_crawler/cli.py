from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
from pathlib import Path

from .config import PipelineConfig
from .deepswe_feedback import append_feedback
from .deepswe_handoff import export_handoff
from .diversity_report import write_diversity_report
from .logging_setup import configure_logging
from .production_events import ProductionEventWriter, read_events


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="alvance-github-crawler",
        description="Collect and verify GitHub repositories using the staged pipeline.",
    )
    parser.add_argument(
        "--query", action="append", help="override a GitHub search query; repeatable"
    )
    parser.add_argument(
        "--max-repos", type=int, help="maximum number of new repositories to process"
    )
    parser.add_argument(
        "--search-pages", type=int, default=None, help="GitHub result pages per query"
    )
    parser.add_argument(
        "--skip-e2b",
        action="store_true",
        help="stop after Docker offline verification and register status=offline_verified",
    )
    parser.add_argument(
        "--retry-rejected",
        action="store_true",
        help="retry repositories with previous terminal rejection records",
    )
    parser.add_argument("--doctor", action="store_true", help="check local tools and credentials")
    parser.add_argument(
        "--package-existing",
        action="store_true",
        help="create Harbor/E2B packages for existing qualified candidates",
    )
    parser.add_argument(
        "--export-deepswe-input",
        action="store_true",
        help="export one registered candidate as a DeepSWE handoff JSON",
    )
    parser.add_argument("--repo", help="repository full name selected by export/events modes")
    parser.add_argument("--out", help="output path selected by export/report modes")
    parser.add_argument(
        "--diversity-report",
        action="store_true",
        help="write a local candidate diversity report without network access",
    )
    parser.add_argument(
        "--record-deepswe-feedback",
        action="store_true",
        help="append one DeepSWE task-production feedback record",
    )
    parser.add_argument("--task-id", help="DeepSWE task id selected by feedback mode")
    parser.add_argument("--base-commit", help="base commit selected by feedback mode")
    parser.add_argument("--outcome", help="feedback outcome, e.g. accepted or abandoned")
    parser.add_argument("--reason", help="feedback reason, e.g. too_shallow or verifier_weak")
    parser.add_argument("--notes", default="", help="short feedback notes")
    parser.add_argument("--events", action="store_true", help="print production events")
    parser.add_argument("--tail", type=int, help="limit events output to the last N rows")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument(
        "--defer-e2b",
        action="store_true",
        help="queue pre-screened candidates without blocking on E2B builds",
    )
    modes.add_argument(
        "--verify-pending",
        action="store_true",
        help="consume queued candidates through E2B, benchmark, and Harbor packaging",
    )
    modes.add_argument(
        "--requeue-failures",
        action="store_true",
        help="reopen completed pending candidates matching a rejection reason",
    )
    parser.add_argument(
        "--failure-reason",
        action="append",
        help="rejection reason selected by --requeue-failures; repeatable",
    )
    parser.add_argument(
        "--failure-contains",
        default="",
        help="optional rejection-log substring selected by --requeue-failures",
    )
    parser.add_argument("--verbose", action="store_true")
    return parser


def doctor(config: PipelineConfig) -> dict[str, object]:
    return {
        "github_token": bool(config.github_token),
        "openai_api_key": bool(config.openai_api_key),
        "openai_base_url": bool(config.openai_base_url),
        "openai_model": config.openai_model,
        "e2b_api_key": bool(config.e2b_api_key),
        "git": shutil.which("git") is not None,
        "docker": shutil.which("docker") is not None,
        "openai_sdk": importlib.util.find_spec("openai") is not None,
        "e2b_sdk": importlib.util.find_spec("e2b") is not None,
        "output_dir": str(config.output_dir),
        "catalog_dir": str(config.catalog_dir),
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging(verbose=args.verbose)
    config = PipelineConfig.from_env()
    if args.search_pages is not None:
        if args.search_pages < 1:
            raise SystemExit("--search-pages must be >= 1")
        config.search_pages = args.search_pages

    if args.doctor:
        print(json.dumps(doctor(config), ensure_ascii=False, indent=2))
        return 0

    if args.export_deepswe_input:
        if not args.repo or not args.out:
            print("--export-deepswe-input requires --repo and --out", file=sys.stderr)
            return 2
        try:
            handoff = export_handoff(config.candidates_path, args.repo, Path(args.out))
        except (OSError, ValueError) as exc:
            print(str(exc), file=sys.stderr)
            return 1
        ProductionEventWriter(config.output_dir / "events.jsonl").emit(
            stage="deepswe_handoff_export",
            event_type="handoff_exported",
            status="ok",
            repo=args.repo,
            output=args.out,
        )
        print(json.dumps(handoff, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if args.diversity_report:
        out = Path(args.out) if args.out else config.catalog_dir / "diversity-report.md"
        try:
            write_diversity_report(
                config.candidates_path,
                out,
                feedback_path=config.catalog_dir / "deepswe-feedback.jsonl",
            )
        except OSError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print(json.dumps({"output": str(out)}, ensure_ascii=False, sort_keys=True))
        return 0

    if args.record_deepswe_feedback:
        missing = [
            label
            for label, value in (
                ("--repo", args.repo),
                ("--base-commit", args.base_commit),
                ("--outcome", args.outcome),
                ("--reason", args.reason),
            )
            if not value
        ]
        if missing:
            print(f"--record-deepswe-feedback requires {', '.join(missing)}", file=sys.stderr)
            return 2
        out = Path(args.out) if args.out else config.catalog_dir / "deepswe-feedback.jsonl"
        feedback = append_feedback(
            out,
            repo=args.repo,
            base_commit=args.base_commit,
            task_id=args.task_id or "",
            outcome=args.outcome,
            reason=args.reason,
            notes=args.notes,
        )
        ProductionEventWriter(config.output_dir / "events.jsonl").emit(
            stage="deepswe_feedback",
            event_type="feedback_recorded",
            status="ok",
            repo=args.repo,
            output=str(out),
            outcome=args.outcome,
            reason=args.reason,
        )
        print(json.dumps(feedback, ensure_ascii=False, sort_keys=True))
        return 0

    if args.events:
        events = read_events(config.output_dir / "events.jsonl")
        if args.repo:
            events = [event for event in events if event.get("repo") == args.repo]
        if args.tail is not None:
            events = events[-args.tail :]
        for event in events:
            print(json.dumps(event, ensure_ascii=False, sort_keys=True))
        return 0

    if args.package_existing:
        if not config.e2b_api_key:
            print("missing required environment variable: E2B_API_KEY", file=sys.stderr)
            return 2
        from .catalog_migration import package_existing_candidates
        from .github import GitHubClient
        from .harbor_packaging import HarborPackager

        stats = package_existing_candidates(
            config.candidates_path,
            HarborPackager(config.e2b_api_key, config.catalog_dir),
            GitHubClient(config.github_token),
        )
        print(json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if args.verify_pending:
        try:
            config.validate(require_e2b=True)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        from .pending_verification import PendingVerificationRunner

        stats = PendingVerificationRunner.from_config(config).run(max_items=args.max_repos)
        print(json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if args.requeue_failures:
        reasons = set(args.failure_reason or [])
        if not reasons:
            print("--requeue-failures requires --failure-reason", file=sys.stderr)
            return 2
        from .pending_queue import PendingQueue
        from .requeue_failures import requeue_failures

        stats = requeue_failures(
            PendingQueue(config.pending_path),
            config.rejections_path,
            reasons=reasons,
            error_contains=args.failure_contains,
        )
        print(json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    try:
        config.validate(require_e2b=not (args.skip_e2b or args.defer_e2b))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    from .pipeline import Pipeline

    pipeline = Pipeline(
        config,
        skip_e2b=args.skip_e2b,
        defer_e2b=args.defer_e2b,
        retry_rejected=args.retry_rejected,
    )
    stats = pipeline.run(queries=args.query, max_repos=args.max_repos)
    print(json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
