from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .jsonl_io import append_text_locked, read_text_locked
from .production_events import utc_now


def append_feedback(
    path: Path,
    *,
    repo: str,
    base_commit: str,
    outcome: str,
    reason: str,
    task_id: str = "",
    material_id: str = "",
    notes: str = "",
) -> dict[str, Any]:
    payload = {
        "schema_version": "0.1",
        "recorded_at": utc_now(),
        "repo": repo,
        "base_commit": base_commit,
        "material_id": material_id or None,
        "task_id": task_id or None,
        "outcome": outcome,
        "reason": reason,
        "notes": notes or None,
    }
    append_text_locked(path, json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    return payload


def read_feedback(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in read_text_locked(path).splitlines():
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            records.append(payload)
    return records


def latest_feedback(path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    latest: dict[tuple[str, str], dict[str, Any]] = {}
    for record in read_feedback(path):
        repo = str(record.get("repo") or "")
        base_commit = str(record.get("base_commit") or "")
        if repo and base_commit:
            latest[(repo, base_commit)] = record
    return latest
