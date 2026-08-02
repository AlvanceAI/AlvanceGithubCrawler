from __future__ import annotations

import json
from pathlib import Path

from ..jsonl_io import split_jsonl_lines
from .queue import PendingQueue


def requeue_failures(
    queue: PendingQueue,
    rejections_path: Path,
    *,
    reasons: set[str],
    error_contains: str = "",
    exclude_repos: set[str] | None = None,
    marker: str = "",
) -> dict[str, int]:
    """Reopen completed pending candidates selected by their latest rejection."""
    latest = latest_rejections(rejections_path)
    exclude = exclude_repos or set()
    stats = {
        "matched": 0,
        "requeued": 0,
        "already_registered": 0,
        "already_requeued": 0,
    }
    used_markers = queue.requeue_markers()
    for key, candidate in queue.candidates_by_key().items():
        repo = candidate.get("repo") or {}
        full_name = str(repo.get("full_name") or "")
        rejection = latest.get(full_name)
        if rejection is None or str(rejection.get("reason")) not in reasons:
            continue
        if error_contains and error_contains not in rejection_text(rejection):
            continue
        if full_name in exclude:
            # The repo failed once but was later registered successfully;
            # reopening it would re-verify and double-register.
            stats["already_registered"] += 1
            continue
        stats["matched"] += 1
        if marker and (key, marker) in used_markers:
            stats["already_requeued"] += 1
        elif queue.requeue(key, marker=marker):
            stats["requeued"] += 1
        else:
            stats["already_requeued"] += 1
    return stats


def latest_rejections(path: Path) -> dict[str, dict[str, object]]:
    latest: dict[str, dict[str, object]] = {}
    if not path.is_file():
        return latest
    for line in split_jsonl_lines(path.read_text(encoding="utf-8")):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        repo = str(record.get("repo") or "")
        if repo:
            latest[repo] = record
    return latest


def rejection_text(rejection: dict[str, object]) -> str:
    offline = rejection.get("offline") or {}
    if not isinstance(offline, dict):
        offline = {}
    return "\n".join(
        str(value or "")
        for value in (
            rejection.get("error"),
            offline.get("stdout_tail"),
            offline.get("stderr_tail"),
        )
    )
