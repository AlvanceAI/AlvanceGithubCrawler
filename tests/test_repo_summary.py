from __future__ import annotations

import json

from alvance_github_crawler.repo_summary import candidate_to_repo_summary, export_repo_summary


def test_export_repo_summary_writes_compact_candidate_metadata(tmp_path) -> None:
    candidates = tmp_path / "candidates.jsonl"
    out = tmp_path / "summary.json"
    record = {
        "repo": "owner/project",
        "base_commit": "abcdef123456",
        "language": "python",
        "license": "MIT",
        "stars": 1234,
        "file_count": 321,
        "soft_score": 9,
        "adjusted_score": 8.5,
        "test_cmd": "pytest",
        "direction": "Improve parser diagnostics.",
        "direction_source": "issue#42",
        "direction_keywords": ["parser", "diagnostics"],
        "direction_target_paths": ["src/parser.py"],
        "taskability": {"score": 7},
        "benchmark": {"test_duration_median_s": 12.3},
        "contamination": {"risk": "medium"},
        "harbor_package": {"material_path": "materials/owner-project"},
    }
    candidates.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")

    summary = export_repo_summary(candidates, "owner/project", out)

    assert summary == candidate_to_repo_summary(record)
    assert summary["repository_url"] == "https://github.com/owner/project"
    assert summary["direction_target_paths"] == ["src/parser.py"]
    assert json.loads(out.read_text(encoding="utf-8"))["taskability"] == {"score": 7}
