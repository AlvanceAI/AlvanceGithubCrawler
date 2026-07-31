from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path

from .artifacts import write_json_atomic
from .config import PipelineConfig
from .deepswe_feedback import append_feedback
from .deepswe_handoff import export_handoff
from .diversity_report import write_diversity_report
from .logging_setup import configure_logging
from .material_export import load_candidate_records, prepare_materials, select_records
from .production_events import ProductionEventWriter, read_events
from .registry import JsonlRegistry
from .repo_summary import export_repo_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="alvance-github-crawler",
        description="Collect and verify GitHub repositories using the staged pipeline.",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=("crawl", "produce"),
        help="run the initial crawl or produce verified tasks from crawl JSONL",
    )
    parser.add_argument(
        "--target-total",
        type=int,
        default=100,
        help="raw GitHub sample size; must equal --per-language multiplied by five",
    )
    parser.add_argument(
        "--per-language",
        type=int,
        default=20,
        help="raw results sampled from each language query; does not cap accepted results",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="outputs/github_crawl_100",
        help="output directory for crawl JSONL and checkpoint files",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="outputs/github_crawl_100/accepted_repositories.jsonl",
        help="accepted crawl JSONL consumed by the produce command",
    )
    parser.add_argument(
        "--repository",
        action="append",
        help="exact repo from --input to produce; repeatable and order-preserving",
    )
    parser.add_argument(
        "--max-search-pages",
        type=int,
        default=10,
        help="maximum GitHub Search pages per language (GitHub caps this at 10)",
    )
    parser.add_argument(
        "--request-interval",
        type=float,
        default=0.2,
        help="minimum seconds between GitHub requests",
    )
    parser.add_argument(
        "--api-timeout",
        type=float,
        default=30.0,
        help="GitHub request timeout in seconds",
    )
    parser.add_argument(
        "--e2b-concurrency",
        type=int,
        default=None,
        help="parallel E2B verifications per API key (1-20; defaults to environment config)",
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
        "--prescreen-concurrency",
        type=int,
        default=None,
        help="parallel repository checkout and direction workers (1-20)",
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
        "--export-repo-summary",
        action="store_true",
        help="export compact candidate metadata for DeepSWE repo-card generation",
    )
    parser.add_argument(
        "--record-deepswe-feedback",
        action="store_true",
        help="append one DeepSWE task-production feedback record",
    )
    parser.add_argument("--task-id", help="DeepSWE task id selected by feedback mode")
    parser.add_argument("--material-id", help="DeepSWE material id selected by feedback mode")
    parser.add_argument("--base-commit", help="base commit selected by feedback mode")
    parser.add_argument("--outcome", help="feedback outcome, e.g. accepted or abandoned")
    parser.add_argument("--reason", help="feedback reason, e.g. too_shallow or verifier_weak")
    parser.add_argument("--notes", default="", help="short feedback notes")
    parser.add_argument("--events", action="store_true", help="print production events")
    parser.add_argument("--tail", type=int, help="limit events output to the last N rows")
    parser.add_argument(
        "--export-materials",
        action="store_true",
        help="prepare a DeepSWE/Harbor Material directory from local crawler outputs",
    )
    parser.add_argument(
        "--repo-count",
        type=int,
        default=5,
        help="number of repositories selected by --export-materials",
    )
    parser.add_argument(
        "--material-dir",
        default="Material",
        help="output directory selected by --export-materials",
    )
    parser.add_argument(
        "--clone-repos",
        action="store_true",
        help="clone selected repositories into the Material directory",
    )
    parser.add_argument(
        "--require-clone",
        action="store_true",
        help="fail --export-materials if any selected repository cannot be cloned",
    )
    parser.add_argument(
        "--clone-timeout-s",
        type=int,
        default=120,
        help="per-command timeout used by --export-materials repository cloning",
    )
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
    socks_proxy = socks_proxy_configured()
    return {
        "github_token": bool(config.github_token),
        "github_token_count": len(config.github_tokens),
        "openai_api_key": bool(config.openai_api_key),
        "openai_base_url": bool(config.openai_base_url),
        "openai_model": config.openai_model,
        "e2b_api_key_count": len(config.e2b_api_keys),
        "e2b_cpu_count": config.e2b_cpu_count,
        "e2b_memory_mb": config.e2b_memory_mb,
        "e2b_concurrency_per_key": config.e2b_concurrency,
        "e2b_total_concurrency": config.e2b_total_concurrency,
        "prescreen_concurrency": config.prescreen_concurrency,
        "language_quota_enabled": config.language_quota_enabled,
        "git": shutil.which("git") is not None,
        "docker": shutil.which("docker") is not None,
        "openai_sdk": importlib.util.find_spec("openai") is not None,
        "e2b_sdk": importlib.util.find_spec("e2b") is not None,
        "socks_proxy_configured": socks_proxy,
        "socks_support": importlib.util.find_spec("socks") is not None,
        "output_dir": str(config.output_dir),
        "catalog_dir": str(config.catalog_dir),
    }


def socks_proxy_configured() -> bool:
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        value = os.getenv(key, "").strip().lower()
        if value.startswith(("socks://", "socks4://", "socks4a://", "socks5://", "socks5h://")):
            return True
    return False


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging(verbose=args.verbose)
    config = PipelineConfig.from_env()
    if args.e2b_concurrency is not None:
        config.e2b_concurrency = args.e2b_concurrency
    if args.search_pages is not None:
        if args.search_pages < 1:
            raise SystemExit("--search-pages must be >= 1")
        config.search_pages = args.search_pages
    if args.prescreen_concurrency is not None:
        config.prescreen_concurrency = args.prescreen_concurrency
    if args.max_repos is not None and args.max_repos < 1:
        raise SystemExit("--max-repos must be >= 1")

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

    if args.export_repo_summary:
        if not args.repo or not args.out:
            print("--export-repo-summary requires --repo and --out", file=sys.stderr)
            return 2
        try:
            summary = export_repo_summary(config.candidates_path, args.repo, Path(args.out))
        except (OSError, ValueError) as exc:
            print(str(exc), file=sys.stderr)
            return 1
        ProductionEventWriter(config.output_dir / "events.jsonl").emit(
            stage="repo_summary_export",
            event_type="repo_summary_exported",
            status="ok",
            repo=args.repo,
            output=args.out,
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
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
            material_id=args.material_id or "",
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

    if args.export_materials:
        if args.repo_count < 1:
            print("--repo-count must be >= 1", file=sys.stderr)
            return 2
        if args.clone_timeout_s < 1:
            print("--clone-timeout-s must be >= 1", file=sys.stderr)
            return 2
        records = load_candidate_records(Path.cwd())
        if args.repo:
            records = [record for record in records if record.get("repo") == args.repo]
            if not records:
                print(f"repo not found in local crawler outputs: {args.repo}", file=sys.stderr)
                return 1
        selected, warnings = select_records(records, args.repo_count)
        if not selected:
            print("no usable local crawler records found", file=sys.stderr)
            return 1
        material_dir = Path(args.out) if args.out else Path(args.material_dir)
        try:
            index = prepare_materials(
                selected,
                crawler_dir=Path.cwd(),
                material_dir=material_dir,
                clone_repos=args.clone_repos,
                require_clone=args.require_clone,
                clone_timeout_s=args.clone_timeout_s,
            )
        except (OSError, RuntimeError) as exc:
            print(str(exc), file=sys.stderr)
            return 1
        summary = {
            "schema_version": "0.1",
            "output": str(material_dir),
            "selected": len(index),
            "warnings": warnings,
            "items": index,
        }
        write_json_atomic(material_dir / "index.json", summary)
        ProductionEventWriter(config.output_dir / "events.jsonl").emit(
            stage="material_export",
            event_type="materials_exported",
            status="ok",
            output=str(material_dir),
            selected=len(index),
            warnings=warnings,
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if args.command == "crawl":
        from .crawl import CandidateCrawler, CrawlIncompleteError
        from .github import GitHubClient, GitHubError

        if not config.github_tokens:
            print(
                "missing required environment variable: GITHUB_TOKEN or GITHUB_TOKEN1/2",
                file=sys.stderr,
            )
            return 2
        try:
            crawler = CandidateCrawler(
                GitHubClient(
                    config.github_tokens,
                    timeout=args.api_timeout,
                    request_interval_s=args.request_interval,
                ),
                Path(args.output),
                target_total=args.target_total,
                per_language=args.per_language,
                max_search_pages=args.max_search_pages,
            )
            summary = crawler.run()
        except (CrawlIncompleteError, GitHubError, ValueError) as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if args.command == "produce":
        from .pipeline import Pipeline

        if args.verify_pending or args.requeue_failures or args.package_existing:
            print(
                "produce cannot be combined with pending, requeue, or package modes",
                file=sys.stderr,
            )
            return 2
        try:
            config.validate(require_e2b=not (args.skip_e2b or args.defer_e2b))
            pipeline = Pipeline(
                config,
                skip_e2b=args.skip_e2b,
                defer_e2b=args.defer_e2b,
                retry_rejected=args.retry_rejected,
            )
            stats = pipeline.run_crawl_candidates(
                Path(args.input),
                max_repos=args.max_repos,
                repositories=args.repository,
            )
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        print(json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if args.package_existing:
        from .catalog.harbor_packaging import HarborPackager
        from .catalog.migration import package_existing_candidates
        from .github import GitHubClient

        if not config.e2b_api_keys:
            print(
                "missing required environment variable: E2B_API_KEY or E2B_API_KEY1/2/3",
                file=sys.stderr,
            )
            return 2
        stats = package_existing_candidates(
            config.candidates_path,
            HarborPackager(
                config.e2b_api_key,
                config.catalog_dir,
                cpu_count=config.e2b_cpu_count,
                memory_mb=config.e2b_memory_mb,
            ),
            GitHubClient(config.github_tokens),
        )
        print(json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if args.verify_pending:
        from .pending.verification import PendingVerificationRunner

        try:
            config.validate(require_e2b=True)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        stats = PendingVerificationRunner.from_config(config).run(
            max_items=args.max_repos,
            max_workers=config.e2b_concurrency,
        )
        print(json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True))
        if (
            int(stats.get("key_slots_exhausted", 0)) >= len(config.e2b_api_keys)
            and int(stats.get("remaining", 0)) > 0
        ):
            return 4
        return 0

    if args.requeue_failures:
        from .pending.queue import PendingQueue
        from .pending.requeue import requeue_failures

        reasons = set(args.failure_reason or [])
        if not reasons:
            print("--requeue-failures requires --failure-reason", file=sys.stderr)
            return 2
        registry = JsonlRegistry(
            config.candidates_path,
            config.rejections_path,
            config.output_dir / "events.jsonl",
        )
        stats = requeue_failures(
            PendingQueue(config.pending_path),
            config.rejections_path,
            reasons=reasons,
            error_contains=args.failure_contains,
            exclude_repos=registry.existing_repos(),
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
