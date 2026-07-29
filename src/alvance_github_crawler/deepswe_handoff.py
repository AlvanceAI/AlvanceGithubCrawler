from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .artifacts import write_json_atomic


def candidate_to_handoff(record: dict[str, Any]) -> dict[str, Any]:
    package = record.get("harbor_package") or {}
    repo = record.get("repo")
    return {
        "schema_version": "0.1",
        "repo": repo,
        "repository_url": record.get("repository_url")
        or (f"https://github.com/{repo}" if repo else None),
        "base_commit": record.get("base_commit"),
        "source_tree": record.get("source_tree"),
        "default_branch": record.get("default_branch"),
        "language": record.get("language"),
        "license": record.get("license"),
        "direction": record.get("direction"),
        "direction_source": record.get("direction_source"),
        "direction_keywords": record.get("direction_keywords") or [],
        "direction_target_paths": record.get("direction_target_paths") or [],
        "h6_sources": record.get("h6_sources") or [],
        "test_cmd": record.get("test_cmd"),
        "e2b_template": record.get("e2b_template"),
        "e2b_environment": record.get("e2b_environment") or {},
        "benchmark": record.get("benchmark") or {},
        "harbor_package": package,
        "material_path": package.get("material_path"),
        "task_path": package.get("task_path"),
        "taskability": record.get("taskability") or {},
        "contamination": record.get("contamination") or {},
    }


def export_handoff(candidates_path: Path, repo: str, out: Path) -> dict[str, Any]:
    record = find_candidate(candidates_path, repo)
    handoff = candidate_to_handoff(record)
    validate_handoff(handoff)
    write_json_atomic(out, handoff)
    return handoff


def find_candidate(candidates_path: Path, repo: str) -> dict[str, Any]:
    if not candidates_path.is_file():
        raise FileNotFoundError(f"candidate registry not found: {candidates_path}")
    latest: dict[str, Any] | None = None
    for line in candidates_path.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if record.get("repo") == repo:
            latest = record
    if latest is None:
        raise ValueError(f"repo not found in candidate registry: {repo}")
    return latest


def validate_handoff(handoff: dict[str, Any]) -> None:
    missing = [
        key
        for key in ("repo", "repository_url", "base_commit", "language", "direction")
        if not handoff.get(key)
    ]
    if missing:
        raise ValueError(f"handoff missing required fields: {', '.join(missing)}")
