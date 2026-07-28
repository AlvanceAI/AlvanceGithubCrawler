from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PENDING_SCHEMA_VERSION = "0.1"
REPO_FIELDS = (
    "full_name",
    "name",
    "description",
    "topics",
    "language",
    "stargazers_count",
    "size",
    "pushed_at",
    "license",
    "default_branch",
    "base_commit",
    "source_tree",
)


@dataclass(frozen=True, slots=True)
class PendingItem:
    key: str
    candidate: dict[str, Any]


class PendingQueue:
    """Append-only control-plane queue for deferred E2B verification."""

    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)

    def enqueue(self, candidate: dict[str, Any]) -> bool:
        key = pending_key(candidate)
        if key in self.known_keys():
            return False
        self._append("queued", key, candidate=candidate)
        return True

    def complete(self, key: str, outcome: str) -> None:
        self._append("completed", key, outcome=outcome)

    def record_attempt(self, key: str, outcome: str = "error") -> None:
        self._append("attempted", key, outcome=outcome)

    def pending(self) -> list[PendingItem]:
        active: dict[str, PendingItem] = {}
        for event in self._events():
            key = str(event.get("key") or "")
            if not key:
                continue
            if event.get("event") == "queued" and isinstance(event.get("candidate"), dict):
                active[key] = PendingItem(key=key, candidate=dict(event["candidate"]))
            elif event.get("event") == "completed":
                active.pop(key, None)
        return list(active.values())

    def known_keys(self) -> set[str]:
        return {str(event["key"]) for event in self._events() if event.get("key")}

    def known_repos(self) -> set[str]:
        repos: set[str] = set()
        for event in self._events():
            candidate = event.get("candidate")
            if not isinstance(candidate, dict):
                continue
            repo = candidate.get("repo")
            if isinstance(repo, dict) and repo.get("full_name"):
                repos.add(str(repo["full_name"]))
        return repos

    def _events(self) -> list[dict[str, Any]]:
        if not self.path.is_file():
            return []
        events: list[dict[str, Any]] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict):
                events.append(event)
        return events

    def _append(self, event: str, key: str, **fields: Any) -> None:
        payload = {
            "schema_version": PENDING_SCHEMA_VERSION,
            "event": event,
            "key": key,
            "recorded_at": datetime.now(UTC).isoformat(),
            **fields,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def build_pending_candidate(
    repo: dict[str, Any],
    score: dict[str, Any],
    direction: dict[str, Any],
) -> dict[str, Any]:
    compact_repo = {field: repo.get(field) for field in REPO_FIELDS}
    return {"repo": compact_repo, "score": score, "direction": direction}


def pending_key(candidate: dict[str, Any]) -> str:
    repo = candidate.get("repo") or {}
    full_name = str(repo.get("full_name") or "")
    commit = str(repo.get("base_commit") or "")
    if not full_name or not commit:
        raise ValueError("pending candidate requires repo.full_name and repo.base_commit")
    return f"{full_name}@{commit}"
