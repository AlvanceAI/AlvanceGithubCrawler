from __future__ import annotations

import json
from pathlib import Path

import pytest

from alvance_github_crawler.models import HardFilterResult
from alvance_github_crawler.pipeline import Pipeline, load_crawl_candidates


def crawl_candidate(repo: str = "owner/library") -> dict[str, object]:
    return {
        "repo": repo,
        "base_commit": "a" * 40,
        "source_tree": "b" * 40,
        "language": "python",
        "stars": 500,
        "license": "MIT",
        "default_branch": "main",
        "pushed_at": "2026-07-01T00:00:00Z",
    }


def test_load_crawl_candidates_selects_requested_order(tmp_path: Path) -> None:
    path = tmp_path / "accepted.jsonl"
    first = crawl_candidate("owner/first")
    second = crawl_candidate("owner/second")
    path.write_text("\n".join(json.dumps(item) for item in (first, second)), encoding="utf-8")

    selected = load_crawl_candidates(path, repositories=["owner/second", "owner/first"])

    assert [item["repo"] for item in selected] == ["owner/second", "owner/first"]


def test_load_crawl_candidates_rejects_non_pinned_records(tmp_path: Path) -> None:
    path = tmp_path / "accepted.jsonl"
    candidate = crawl_candidate()
    candidate["base_commit"] = "short"
    path.write_text(json.dumps(candidate), encoding="utf-8")

    with pytest.raises(ValueError, match="full commit SHA"):
        load_crawl_candidates(path)


class _PinnedGitHub:
    def __init__(self) -> None:
        self.tree_refs: list[str] = []

    def get_head_sha(self, repo: dict[str, object]) -> str:
        raise AssertionError("a crawled candidate must not be replaced with HEAD")

    def get_tree(self, full_name: str, ref: str) -> list[dict[str, object]]:
        self.tree_refs.append(ref)
        return []


class _RejectingFilter:
    @staticmethod
    def evaluate(repo: dict[str, object], tree: list[dict[str, object]]) -> HardFilterResult:
        return HardFilterResult(False, "no_test_infra")


class _Registry:
    def __init__(self) -> None:
        self.rejections: list[tuple[dict[str, object], str, str]] = []

    def reject(self, repo: dict[str, object], stage: str, reason: str, **_: object) -> None:
        self.rejections.append((repo, stage, reason))


def test_process_repo_uses_crawled_commit_without_fetching_head() -> None:
    pipeline = object.__new__(Pipeline)
    pipeline.github = _PinnedGitHub()
    pipeline.hard_filter = _RejectingFilter()
    pipeline.registry = _Registry()
    commit = "c" * 40

    outcome = pipeline._process_repo(
        {
            "full_name": "owner/library",
            "base_commit": commit,
            "source_tree": "d" * 40,
        }
    )

    assert outcome == "rejected"
    assert pipeline.github.tree_refs == [commit]
    assert pipeline.registry.rejections[0][1:] == ("stage1_hard_filter", "no_test_infra")
