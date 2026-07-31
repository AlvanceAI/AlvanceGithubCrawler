from __future__ import annotations

import json

import pytest

from alvance_github_crawler.deepswe_handoff import (
    candidate_to_handoff,
    export_handoff,
    find_candidate,
)


def test_export_handoff_uses_latest_candidate_record(tmp_path) -> None:
    candidates = tmp_path / "candidates.jsonl"
    out = tmp_path / "handoff" / "owner-project.json"
    old_record = {
        "repo": "owner/project",
        "base_commit": "11111111",
        "language": "python",
        "direction": "Old direction",
    }
    latest_record = {
        "repo": "owner/project",
        "base_commit": "222222223333",
        "source_tree": "src/",
        "default_branch": "main",
        "language": "python",
        "license": "MIT",
        "direction": "Tighten parser error handling.",
        "direction_source": "h6",
        "direction_keywords": ["parser", "error"],
        "direction_target_paths": ["src/parser.py"],
        "h6_sources": ["README"],
        "test_cmd": "pytest",
        "e2b_template": "tmpl-1",
        "benchmark": {"test_duration_median_s": 12.3},
        "harbor_package": {
            "material_path": "materials/owner-project",
            "task_path": "tasks/owner-project",
        },
        "taskability": {"score": 4},
        "contamination": {"risk": "unknown"},
    }
    candidates.write_text(
        "".join(
            json.dumps(record, ensure_ascii=False) + "\n"
            for record in [old_record, latest_record]
        ),
        encoding="utf-8",
    )

    handoff = export_handoff(candidates, "owner/project", out)

    assert handoff == candidate_to_handoff(latest_record)
    assert handoff["base_commit"] == "222222223333"
    assert handoff["repository_url"] == "https://github.com/owner/project"
    assert json.loads(out.read_text(encoding="utf-8"))["task_path"] == "tasks/owner-project"


def test_find_candidate_reports_missing_repo(tmp_path) -> None:
    candidates = tmp_path / "candidates.jsonl"
    candidates.write_text('{"repo": "owner/project"}\n', encoding="utf-8")

    with pytest.raises(ValueError, match="repo not found"):
        find_candidate(candidates, "missing/repo")


def test_export_handoff_requires_deepswe_fields(tmp_path) -> None:
    candidates = tmp_path / "candidates.jsonl"
    candidates.write_text(
        json.dumps({"repo": "owner/project", "base_commit": "abc", "language": "python"})
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="direction"):
        export_handoff(candidates, "owner/project", tmp_path / "handoff.json")
