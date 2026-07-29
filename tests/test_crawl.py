from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from alvance_github_crawler.crawl import CandidateCrawler

LANGUAGE_NAMES = {
    "python": "Python",
    "go": "Go",
    "typescript": "TypeScript",
    "javascript": "JavaScript",
    "rust": "Rust",
}


class FakeGitHub:
    def __init__(self) -> None:
        self.request_count = 0
        self.retry_count = 0
        self.rate_limits: dict[str, dict[str, int]] = {}
        self.search_calls = 0

    def search_repositories_page(self, query: str, *, page: int, per_page: int) -> dict[str, Any]:
        self.request_count += 1
        self.search_calls += 1
        language = next(key for key, name in LANGUAGE_NAMES.items() if f"language:{name}" in query)
        items = [self._repo(language), self._repo(language, suffix="second")]
        if language == "python":
            items[1]["license"] = {"spdx_id": "GPL-3.0"}
            items[1]["stargazers_count"] = 10_000
        return {"items": items, "total_count": len(items)}

    def get_head_commit(self, repo: dict[str, Any]) -> dict[str, str]:
        self.request_count += 1
        digest = hashlib.sha1(str(repo["full_name"]).encode()).hexdigest()
        return {
            "sha": digest,
            "tree_sha": hashlib.sha1((digest + "tree").encode()).hexdigest(),
            "committed_at": "2026-07-20T00:00:00Z",
        }

    def get_tree(self, full_name: str, ref: str) -> list[dict[str, Any]]:
        self.request_count += 1
        language = full_name.split("/")[1].split("-")[0]
        paths = {
            "python": ("pyproject.toml", "tests/test_api.py"),
            "go": ("go.mod", "api_test.go", "api.go"),
            "typescript": ("package.json", "src/index.ts"),
            "javascript": ("package.json", "src/index.js"),
            "rust": ("Cargo.toml", "tests/api.rs", "src/lib.rs"),
        }[language]
        return [{"type": "blob", "path": path, "size": 10} for path in paths]

    def get_file(self, full_name: str, path: str, *, ref: str | None = None) -> str | None:
        self.request_count += 1
        if path == "package.json":
            return json.dumps(
                {
                    "scripts": {"test": "vitest run"},
                    "devDependencies": {"vitest": "1.0.0"},
                }
            )
        return None

    def get_rate_limit_status(self) -> dict[str, int]:
        self.request_count += 1
        return {"core": 4_900, "search": 25, "code_search": 10}

    @staticmethod
    def _repo(language: str, suffix: str = "candidate") -> dict[str, Any]:
        return {
            "full_name": f"owner/{language}-{suffix}",
            "name": f"{language}-{suffix}",
            "html_url": f"https://github.com/owner/{language}-{suffix}",
            "language": LANGUAGE_NAMES[language],
            "stargazers_count": 500,
            "license": {"spdx_id": "MIT"},
            "description": "Developer library and SDK toolkit",
            "topics": ["library"],
            "default_branch": "main",
            "pushed_at": "2026-07-20T00:00:00Z",
            "fork": False,
            "archived": False,
            "mirror_url": None,
        }


def test_crawl_filters_complete_raw_sample_without_acceptance_quotas(tmp_path: Path) -> None:
    github = FakeGitHub()
    crawler = CandidateCrawler(
        github,
        tmp_path,
        target_total=10,
        per_language=2,
        max_search_pages=1,
        now=datetime(2026, 7, 29, tzinfo=UTC),
    )

    summary = crawler.run()

    accepted = [
        json.loads(line)
        for line in (tmp_path / "accepted_repositories.jsonl").read_text().splitlines()
    ]
    rejected = [
        json.loads(line)
        for line in (tmp_path / "rejected_repositories.jsonl").read_text().splitlines()
    ]
    assert summary["status"] == "completed"
    assert summary["fetched_total"] == 10
    assert summary["accepted_total"] == 9
    assert summary["accepted_by_language"] == {
        "python": 1,
        "go": 2,
        "typescript": 2,
        "javascript": 2,
        "rust": 2,
    }
    assert len({item["repo"] for item in accepted}) == 9
    assert all(len(item["base_commit"]) == 40 for item in accepted)
    assert all(item["test_evidence"] for item in accepted)
    assert [item["reason"] for item in rejected] == ["unsupported_license"]
    assert len(accepted) + len(rejected) == 10

    resumed_github = FakeGitHub()
    resumed = CandidateCrawler(
        resumed_github,
        tmp_path,
        target_total=10,
        per_language=2,
        max_search_pages=1,
        now=datetime(2026, 8, 1, tzinfo=UTC),
    ).run()

    assert resumed["accepted_total"] == 9
    assert resumed["cutoff_time"] == summary["cutoff_time"]
    assert resumed == summary
    assert resumed_github.search_calls == 0
