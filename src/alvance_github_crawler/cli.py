from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
from pathlib import Path

from .catalog.harbor_packaging import HarborPackager
from .catalog.migration import package_existing_candidates
from .config import PipelineConfig
from .crawl import CandidateCrawler, CrawlIncompleteError
from .github import GitHubClient, GitHubError
from .logging_setup import configure_logging
from .pending.queue import PendingQueue
from .pending.requeue import requeue_failures
from .pending.verification import PendingVerificationRunner
from .pipeline import Pipeline
from .registry import JsonlRegistry


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
        "output_dir": str(config.output_dir),
        "catalog_dir": str(config.catalog_dir),
    }


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

    if args.command == "crawl":
        if not config.github_token:
            print("missing required environment variable: GITHUB_TOKEN", file=sys.stderr)
            return 2
        try:
            crawler = CandidateCrawler(
                GitHubClient(
                    config.github_token,
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

    if args.doctor:
        print(json.dumps(doctor(config), ensure_ascii=False, indent=2))
        return 0

    if args.package_existing:
        if not config.e2b_api_keys:
            print(
                "missing required environment variable: E2B_API_KEY or E2B_API_KEY1/2",
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
        reasons = set(args.failure_reason or [])
        if not reasons:
            print("--requeue-failures requires --failure-reason", file=sys.stderr)
            return 2
        registry = JsonlRegistry(config.candidates_path, config.rejections_path)
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
