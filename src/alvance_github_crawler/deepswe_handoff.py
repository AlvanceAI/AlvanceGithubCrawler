from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .artifacts import write_json_atomic
from .jsonl_io import read_text_locked


def candidate_to_handoff(record: dict[str, Any]) -> dict[str, Any]:
    package = candidate_package(record)
    repo = record.get("repo")
    return {
        "schema_version": "0.1",
        "repo": repo,
        "repository_url": candidate_repository_url(record),
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
        "e2b_template": source_template_alias(record),
        "e2b_environment": candidate_environment(record),
        "benchmark": record.get("benchmark") or record.get("verification") or {},
        "harbor_package": package,
        "material_path": package.get("material_path") or record.get("material_path"),
        "task_path": package.get("task_path") or record.get("task_path"),
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
    for line in read_text_locked(candidates_path).splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict) and record.get("repo") == repo:
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


def candidate_repository_url(record: dict[str, Any]) -> str | None:
    repo = record.get("repo")
    return record.get("repository_url") or (f"https://github.com/{repo}" if repo else None)


def candidate_package(record: dict[str, Any]) -> dict[str, Any]:
    package = dict(record.get("harbor_package") or {})
    material_path = package.get("material_path") or record.get("material_path")
    task_path = package.get("task_path") or record.get("task_path")
    if material_path:
        package["material_path"] = material_path
    if task_path:
        package["task_path"] = task_path
    harbor = package.get("harbor") or record.get("harbor")
    if harbor:
        package["harbor"] = harbor
    history = package.get("e2b_history") or record.get("e2b_history")
    if history:
        package["e2b_history"] = history
    return package


def candidate_environment(record: dict[str, Any]) -> dict[str, Any]:
    environment = record.get("e2b_environment")
    if isinstance(environment, dict) and environment:
        return environment
    resources = record.get("resources") or {}
    inferred = {
        "runtime_version": record.get("runtime_version"),
        "runtime_env": record.get("runtime_env"),
        "execution_user": record.get("execution_user"),
        "cpu_count": resources.get("cpu_count") if isinstance(resources, dict) else None,
        "memory_mb": resources.get("memory_mb") if isinstance(resources, dict) else None,
    }
    return {key: value for key, value in inferred.items() if value not in (None, "", {})}


def source_template_alias(record: dict[str, Any]) -> str | None:
    history = record.get("e2b_history") or {}
    source_template = record.get("source_template") or {}
    if isinstance(history, dict):
        history_source = history.get("source_template") or {}
        if isinstance(history_source, dict) and history_source.get("alias"):
            return str(history_source["alias"])
    if isinstance(source_template, dict) and source_template.get("alias"):
        return str(source_template["alias"])
    raw = record.get("e2b_template")
    return str(raw) if raw else None
