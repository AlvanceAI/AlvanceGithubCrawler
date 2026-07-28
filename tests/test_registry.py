from __future__ import annotations

import json

from alvance_github_crawler.registry import JsonlRegistry


def test_registry_round_trip(tmp_path) -> None:
    registry = JsonlRegistry(tmp_path / "candidates.jsonl", tmp_path / "rejections.jsonl")
    registry.register({"repo": "owner/repo", "language": "go"})
    registry.reject({"full_name": "bad/repo"}, "stage1", "license")
    registry.reject({"full_name": "retry/repo"}, "stage3", "stage_error")

    assert registry.existing_repos() == {"owner/repo"}
    assert registry.terminal_rejections() == {"bad/repo"}
    rejection = json.loads(
        (tmp_path / "rejections.jsonl").read_text(encoding="utf-8").splitlines()[0]
    )
    assert rejection["reason"] == "license"
