from __future__ import annotations

from pathlib import Path
from typing import Any

from .artifacts import write_json_atomic
from .deepswe_handoff import (
    candidate_package,
    candidate_repository_url,
    find_candidate,
)


def candidate_to_repo_summary(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "repo": record.get("repo"),
        "repository_url": candidate_repository_url(record),
        "base_commit": record.get("base_commit"),
        "source_tree": record.get("source_tree"),
        "default_branch": record.get("default_branch"),
        "language": record.get("language"),
        "license": record.get("license"),
        "stars": record.get("stars"),
        "file_count": record.get("file_count"),
        "soft_score": record.get("soft_score"),
        "adjusted_score": record.get("adjusted_score"),
        "test_cmd": record.get("test_cmd"),
        "direction": record.get("direction"),
        "direction_source": record.get("direction_source"),
        "direction_keywords": record.get("direction_keywords") or [],
        "direction_target_paths": record.get("direction_target_paths") or [],
        "taskability": record.get("taskability") or {},
        "benchmark": record.get("benchmark") or record.get("verification") or {},
        "contamination": record.get("contamination") or {},
        "harbor_package": candidate_package(record),
    }


def export_repo_summary(candidates_path: Path, repo: str, out: Path) -> dict[str, Any]:
    summary = candidate_to_repo_summary(find_candidate(candidates_path, repo))
    write_json_atomic(out, summary)
    return summary
