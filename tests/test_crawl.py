from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import alvance_github_crawler.crawl as crawl_module
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
        items = [
            self._repo(language, suffix=f"candidate-{page}"),
            self._repo(language, suffix=f"second-{page}"),
        ]
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


def test_crawl_durably_persists_raw_pages(tmp_path: Path, monkeypatch: Any) -> None:
    calls: list[tuple[str, bool]] = []
    original_append = crawl_module.append_text_locked

    def record_append(path: Path, payload: str, *, durable: bool = False) -> None:
        calls.append((path.name, durable))
        original_append(path, payload, durable=durable)

    monkeypatch.setattr(crawl_module, "append_text_locked", record_append)

    CandidateCrawler(
        FakeGitHub(),
        tmp_path,
        target_total=5,
        per_language=1,
        max_search_pages=1,
        now=datetime(2026, 7, 29, tzinfo=UTC),
    ).run()

    raw_calls = [durable for name, durable in calls if name == "raw_repositories.jsonl"]
    result_calls = [
        durable
        for name, durable in calls
        if name in {"accepted_repositories.jsonl", "rejected_repositories.jsonl"}
    ]
    assert raw_calls == [True] * 5
    assert result_calls
    assert not any(result_calls)


def test_crawl_keeps_unicode_line_separator_inside_json_record(tmp_path: Path) -> None:
    class UnicodeDescriptionGitHub(FakeGitHub):
        def search_repositories_page(
            self,
            query: str,
            *,
            page: int,
            per_page: int,
        ) -> dict[str, Any]:
            payload = super().search_repositories_page(query, page=page, per_page=per_page)
            if "language:TypeScript" in query:
                payload["items"][0]["description"] = "video to\u2028ASCII frames"
            return payload

    summary = CandidateCrawler(
        UnicodeDescriptionGitHub(),
        tmp_path,
        target_total=5,
        per_language=1,
        max_search_pages=1,
        now=datetime(2026, 7, 29, tzinfo=UTC),
    ).run()

    assert summary["status"] == "completed"
    assert summary["fetched_total"] == 5
    assert summary["accepted_total"] == 5
    state = json.loads((tmp_path / "crawl_state.json").read_text(encoding="utf-8"))
    assert state["raw_counts_by_language"] == {
        "python": 1,
        "go": 1,
        "typescript": 1,
        "javascript": 1,
        "rust": 1,
    }
    assert state["processed_total"] == 5


def test_crawl_redistributes_an_exhausted_language_target(tmp_path: Path) -> None:
    class ExhaustedRustGitHub(FakeGitHub):
        def search_repositories_page(
            self,
            query: str,
            *,
            page: int,
            per_page: int,
        ) -> dict[str, Any]:
            if "language:Rust" not in query:
                return super().search_repositories_page(query, page=page, per_page=per_page)
            self.request_count += 1
            self.search_calls += 1
            if page != 1:
                return {"items": [], "total_count": 1}
            item = self._repo("rust", suffix="only-result")
            item["pushed_at"] = "2025-07-29T00:00:00Z"
            return {"items": [item], "total_count": 1}

    github = ExhaustedRustGitHub()
    summary = CandidateCrawler(
        github,
        tmp_path,
        target_total=15,
        per_language=3,
        max_search_pages=3,
        now=datetime(2026, 7, 29, tzinfo=UTC),
    ).run()

    assert summary["status"] == "completed"
    assert summary["fetched_total"] == 15
    assert summary["exhausted_languages"] == ["rust"]
    assert summary["raw_targets_by_language"] == {
        "python": 4,
        "go": 4,
        "typescript": 3,
        "javascript": 3,
        "rust": 1,
    }
    assert summary["validation_errors"] == []

    resumed_github = ExhaustedRustGitHub()
    resumed = CandidateCrawler(
        resumed_github,
        tmp_path,
        target_total=15,
        per_language=3,
        max_search_pages=3,
        now=datetime(2026, 8, 1, tzinfo=UTC),
    ).run()
    assert resumed == summary
    assert resumed_github.search_calls == 0

    expanded = CandidateCrawler(
        ExhaustedRustGitHub(),
        tmp_path,
        target_total=20,
        per_language=4,
        max_search_pages=5,
        now=datetime(2026, 8, 1, tzinfo=UTC),
    ).run()
    assert expanded["status"] == "completed"
    assert expanded["fetched_total"] == 20
    assert expanded["exhausted_languages"] == ["rust"]
    assert expanded["raw_targets_by_language"] == {
        "python": 5,
        "go": 5,
        "typescript": 5,
        "javascript": 4,
        "rust": 1,
    }


def test_crawl_completes_with_available_sample_when_all_languages_exhausted(
    tmp_path: Path,
) -> None:
    class ExhaustedGitHub(FakeGitHub):
        def search_repositories_page(
            self,
            query: str,
            *,
            page: int,
            per_page: int,
        ) -> dict[str, Any]:
            self.request_count += 1
            self.search_calls += 1
            language = next(
                key for key, name in LANGUAGE_NAMES.items() if f"language:{name}" in query
            )
            if page > 1:
                return {"items": [], "total_count": 0}
            item = self._repo(language, suffix="only-result")
            item["pushed_at"] = "2025-07-30T00:00:00Z"
            return {"items": [item], "total_count": 1}

    summary = CandidateCrawler(
        ExhaustedGitHub(),
        tmp_path,
        target_total=10,
        per_language=2,
        max_search_pages=1,
        now=datetime(2026, 7, 29, tzinfo=UTC),
    ).run()

    assert summary["status"] == "completed"
    assert summary["exhausted_without_full_target"] is True
    assert summary["target_total"] == 10
    assert summary["fetched_total"] == 5
    assert summary["accepted_total"] + summary["rejected_total"] == 5
    assert summary["validation_errors"] == []

    resumed = CandidateCrawler(
        ExhaustedGitHub(),
        tmp_path,
        target_total=10,
        per_language=2,
        max_search_pages=1,
        now=datetime(2026, 8, 1, tzinfo=UTC),
    ).run()
    assert resumed == summary


def test_completed_checkpoint_can_expand_to_more_search_pages(tmp_path: Path) -> None:
    initial = CandidateCrawler(
        FakeGitHub(),
        tmp_path,
        target_total=5,
        per_language=1,
        max_search_pages=2,
        now=datetime(2026, 7, 29, tzinfo=UTC),
    ).run()
    expanded_github = FakeGitHub()

    expanded = CandidateCrawler(
        expanded_github,
        tmp_path,
        target_total=10,
        per_language=2,
        max_search_pages=2,
        now=datetime(2026, 8, 1, tzinfo=UTC),
    ).run()

    assert initial["fetched_total"] == 5
    assert expanded["fetched_total"] == 10
    assert expanded["target_total"] == 10
    assert expanded["cutoff_time"] == initial["cutoff_time"]
    assert expanded_github.search_calls == 5


def test_crawl_advances_to_older_search_windows(tmp_path: Path) -> None:
    class WindowedFakeGitHub(FakeGitHub):
        def __init__(self) -> None:
            super().__init__()
            self.queries: list[str] = []

        def search_repositories_page(
            self,
            query: str,
            *,
            page: int,
            per_page: int,
        ) -> dict[str, Any]:
            self.request_count += 1
            self.search_calls += 1
            self.queries.append(query)
            language = next(
                key for key, name in LANGUAGE_NAMES.items() if f"language:{name}" in query
            )
            older_window = ".." in query
            window = "older" if older_window else "newer"
            pushed_at = "2026-06-20T00:00:00Z" if older_window else "2026-07-20T00:00:00Z"
            items = [
                self._repo(language, suffix=f"{window}-first"),
                self._repo(language, suffix=f"{window}-second"),
            ]
            for item in items:
                item["pushed_at"] = pushed_at
            return {"items": items, "total_count": len(items)}

    github = WindowedFakeGitHub()
    summary = CandidateCrawler(
        github,
        tmp_path,
        target_total=15,
        per_language=3,
        max_search_pages=1,
        now=datetime(2026, 7, 29, tzinfo=UTC),
    ).run()

    assert summary["status"] == "completed"
    assert summary["fetched_total"] == 15
    assert summary["search_windows_used"] == {language: 2 for language in LANGUAGE_NAMES}
    assert github.search_calls == 10
    older_queries = [query for query in github.queries if ".." in query]
    assert len(older_queries) == 5
    assert all(query.count("pushed:") == 1 for query in older_queries)
    assert all("T" not in query.split("pushed:", 1)[1] for query in older_queries)


def test_crawl_migrates_timestamp_search_boundaries(tmp_path: Path) -> None:
    state = {
        "schema_version": "1.2",
        "selection_semantics": "raw_sample_all_pass_v1",
        "target_total": 5,
        "per_language": 1,
        "started_at": "2026-07-29T09:08:23Z",
        "cutoff_time": "2025-07-29T09:08:23Z",
        "next_page_by_language": {language: 7 for language in LANGUAGE_NAMES},
        "pushed_before_by_language": {
            language: "2026-07-29T12:47:08Z" for language in LANGUAGE_NAMES
        },
        "search_windows_by_language": {language: 2 for language in LANGUAGE_NAMES},
        "search_pages_fetched_by_language": {language: 16 for language in LANGUAGE_NAMES},
        "api_request_count": 100,
        "retry_count": 0,
        "completed": False,
    }
    (tmp_path / "crawl_state.json").write_text(json.dumps(state), encoding="utf-8")
    crawler = CandidateCrawler(
        FakeGitHub(),
        tmp_path,
        target_total=10,
        per_language=2,
        max_search_pages=10,
        now=datetime(2026, 7, 30, tzinfo=UTC),
    )

    migrated = crawler._load_state([])

    assert migrated["schema_version"] == "1.4"
    assert migrated["allocation_semantics"] == (
        "balanced_with_exhaustion_redistribution_v1"
    )
    assert migrated["pushed_before_by_language"] == {
        language: "2026-07-29" for language in LANGUAGE_NAMES
    }
    assert migrated["next_page_by_language"] == {
        language: 1 for language in LANGUAGE_NAMES
    }
