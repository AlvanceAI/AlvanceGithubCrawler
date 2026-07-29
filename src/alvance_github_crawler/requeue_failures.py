from __future__ import annotations

import json
from pathlib import Path

from .pending_queue import PendingQueue


def requeue_failures(
    queue: PendingQueue,
    rejections_path: Path,
    *,
    reasons: set[str],
    error_contains: str = "",
) -> dict[str, int]:
    """Reopen completed pending candidates selected by their latest rejection."""
    latest = latest_rejections(rejections_path)
    stats = {"matched": 0, "requeued": 0}
    for key, candidate in queue.candidates_by_key().items():
        repo = candidate.get("repo") or {}
        rejection = latest.get(str(repo.get("full_name") or ""))
        if rejection is None or str(rejection.get("reason")) not in reasons:
            continue
        if error_contains and error_contains not in rejection_text(rejection):
            continue
        stats["matched"] += 1
        if queue.requeue(key):
            stats["requeued"] += 1
    return stats


def latest_rejections(path: Path) -> dict[str, dict[str, object]]:
    latest: dict[str, dict[str, object]] = {}
    if not path.is_file():
        return latest
    for line in path.read_text(encoding="utf-8").splitlines():
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
