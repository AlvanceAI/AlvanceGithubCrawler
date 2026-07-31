from __future__ import annotations

import json

from alvance_github_crawler.diversity_report import build_diversity_report, write_diversity_report


def test_diversity_report_summarizes_candidate_distribution(tmp_path) -> None:
    candidates = tmp_path / "candidates.jsonl"
    feedback = tmp_path / "feedback.jsonl"
    out = tmp_path / "reports" / "diversity.md"
    records = [
        {
            "repo": "a/one",
            "base_commit": "1",
            "language": "python",
            "taskability": {"score": 7},
            "contamination": {"risk": "low"},
            "direction_target_paths": ["src/parser.py"],
        },
        {
            "repo": "b/two",
            "base_commit": "2",
            "language": "python",
            "taskability": {"score": 4},
            "contamination": {"risk": "medium"},
            "direction_target_paths": ["docs/config.md"],
        },
        {
            "repo": "c/three",
            "base_commit": "3",
            "language": "go",
            "taskability": {"score": 1, "risk": ["low_taskability"]},
            "direction_target_paths": ["pkg/parser.go"],
        },
    ]
    candidates.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )
    feedback.write_text(
        json.dumps({"repo": "a/one", "base_commit": "1", "outcome": "abandoned"}) + "\n",
        encoding="utf-8",
    )

    report = write_diversity_report(candidates, out, feedback_path=feedback)

    assert report == out.read_text(encoding="utf-8")
    assert "- Candidates: 3" in report
    assert "- Abandoned feedback records: 1" in report
    assert "`python`: 2" in report
    assert "`high`: 1" in report
    assert "`medium`: 1" in report
    assert "`low_taskability`: 1" in report
    assert "`implementation`: 2" in report
    assert "`low_value`: 1" in report
    assert "`a/one@1`" in report
    assert "python exceeds 40% of candidates" in report
    assert "medium contamination risk candidates: 1" in report


def test_empty_diversity_report_is_still_renderable(tmp_path) -> None:
    report = build_diversity_report(tmp_path / "missing.jsonl")

    assert "- Candidates: 0" in report
    assert "## Languages" in report
    assert "- none" in report
