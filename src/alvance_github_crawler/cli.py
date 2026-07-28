from __future__ import annotations

import argparse
import importlib.util
import json
import logging
import shutil
import sys

from .config import PipelineConfig
from .harbor_packaging import HarborPackager
from .pipeline import Pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="alvance-github-crawler",
        description="Collect and verify GitHub repositories using the staged pipeline.",
    )
    parser.add_argument("--query", action="append", help="override a GitHub search query; repeatable")
    parser.add_argument("--max-repos", type=int, help="maximum number of new repositories to process")
    parser.add_argument("--search-pages", type=int, default=None, help="GitHub result pages per query")
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
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    config = PipelineConfig.from_env()
    if args.search_pages is not None:
        if args.search_pages < 1:
            raise SystemExit("--search-pages must be >= 1")
        config.search_pages = args.search_pages

    if args.doctor:
        print(json.dumps(doctor(config), ensure_ascii=False, indent=2))
        return 0

    if args.package_existing:
        if not config.e2b_api_key:
            print("missing required environment variable: E2B_API_KEY", file=sys.stderr)
            return 2
        stats = HarborPackager(config.e2b_api_key, config.catalog_dir).package_existing(
            config.candidates_path
        )
        print(json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    try:
        config.validate(require_e2b=not args.skip_e2b)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    pipeline = Pipeline(
        config,
        skip_e2b=args.skip_e2b,
        retry_rejected=args.retry_rejected,
    )
    stats = pipeline.run(queries=args.query, max_repos=args.max_repos)
    print(json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
