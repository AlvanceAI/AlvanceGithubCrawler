from __future__ import annotations

from alvance_github_crawler.taskability import evaluate_taskability


def test_taskability_rewards_implementation_rich_repositories() -> None:
    result = evaluate_taskability(
        {
            "name": "config-parser",
            "description": "SDK client with parser and cache behavior",
            "topics": ["cli", "serializer"],
        },
        direction={
            "direction": "Refactor protocol config parsing.",
            "target_paths": ["src/parser.py"],
        },
        benchmark={"test_duration_median_s": 42},
    )

    assert result["score"] >= 5
    assert "parser" in result["signals"]
    assert "test_budget_ok" in result["signals"]
    assert result["risk"] == []


def test_taskability_penalizes_doc_only_targets() -> None:
    result = evaluate_taskability(
        {"name": "docs-site", "description": "examples and docs", "topics": []},
        direction={"direction": "Improve docs.", "target_paths": ["docs/usage.md"]},
        benchmark={},
    )

    assert result["score"] <= 1
    assert "low_taskability" in result["risk"]
