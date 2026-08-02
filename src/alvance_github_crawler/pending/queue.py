from __future__ import annotations

import fcntl
import json
import threading
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from ..jsonl_io import append_text_locked, read_text_locked, split_jsonl_lines

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
    retry_at: datetime | None = None


class PendingQueue:
    """Append-only control-plane queue for deferred E2B verification."""

    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self._cache_lock = threading.RLock()
        self._active_keys_cache: set[str] | None = None
        self._cache_offset = 0
        self._cache_inode: int | None = None

    def enqueue(self, candidate: dict[str, Any]) -> bool:
        key = pending_key(candidate)
        with self._cache_lock:
            if key in self._active_keys():
                return False
            self._append("queued", key, candidate=candidate)
            if self._active_keys_cache is not None:
                self._active_keys_cache.add(key)
            return True

    def requeue(self, key: str, *, marker: str = "") -> bool:
        candidate = self.candidates_by_key().get(key)
        if (
            candidate is None
            or key in {item.key for item in self.pending()}
            or (marker and (key, marker) in self.requeue_markers())
        ):
            return False
        self._append("requeued", key, candidate=candidate, requeue_marker=marker)
        return True

    def complete(self, key: str, outcome: str) -> None:
        self._append("completed", key, outcome=outcome)

    def record_attempt(self, key: str, outcome: str = "error") -> None:
        self._append("attempted", key, outcome=outcome)

    def defer(self, key: str, *, delay_s: int = 0) -> None:
        """Move a still-active item to the tail of the queue."""
        retry_at = ""
        if delay_s > 0:
            retry_at = (datetime.now(UTC) + timedelta(seconds=delay_s)).isoformat()
        self._append("deferred", key, retry_at=retry_at)

    def attempt_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for event in self._events():
            key = str(event.get("key") or "")
            if not key:
                continue
            if event.get("event") in {"queued", "requeued"}:
                counts.pop(key, None)
            elif event.get("event") == "attempted":
                counts[key] = counts.get(key, 0) + 1
        return counts

    def pending(self) -> list[PendingItem]:
        active: dict[str, PendingItem] = {}
        for event in self._events():
            key = str(event.get("key") or "")
            if not key:
                continue
            if event.get("event") in {"queued", "requeued"} and isinstance(
                event.get("candidate"), dict
            ):
                active[key] = PendingItem(key=key, candidate=dict(event["candidate"]))
            elif event.get("event") == "deferred":
                item = active.pop(key, None)
                if item is not None:
                    active[key] = PendingItem(
                        key=item.key,
                        candidate=item.candidate,
                        retry_at=_parse_datetime(event.get("retry_at")),
                    )
            elif event.get("event") == "completed":
                active.pop(key, None)
        return list(active.values())

    def active_count(self) -> int:
        """Return active depth without replaying the complete event history."""
        return len(self._active_keys())

    def ready(self, *, now: datetime | None = None) -> list[PendingItem]:
        current = now or datetime.now(UTC)
        return [
            item
            for item in self.pending()
            if item.retry_at is None or item.retry_at <= current
        ]

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

    def active_repos(self) -> set[str]:
        """Repositories with an item still waiting in the queue."""
        repos: set[str] = set()
        for item in self.pending():
            repo = item.candidate.get("repo")
            if isinstance(repo, dict) and repo.get("full_name"):
                repos.add(str(repo["full_name"]))
        return repos

    def candidates_by_key(self) -> dict[str, dict[str, Any]]:
        candidates: dict[str, dict[str, Any]] = {}
        for event in self._events():
            candidate = event.get("candidate")
            if event.get("key") and isinstance(candidate, dict):
                candidates[str(event["key"])] = dict(candidate)
        return candidates

    def requeue_markers(self) -> set[tuple[str, str]]:
        markers: set[tuple[str, str]] = set()
        for event in self._events():
            key = str(event.get("key") or "")
            marker = str(event.get("requeue_marker") or "")
            if key and marker:
                markers.add((key, marker))
        return markers

    def _events(self) -> list[dict[str, Any]]:
        if not self.path.is_file():
            return []
        events: list[dict[str, Any]] = []
        for line in split_jsonl_lines(read_text_locked(self.path)):
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict):
                events.append(event)
        return events

    def _active_keys(self) -> set[str]:
        """Maintain a lightweight active-key index for concurrent enqueue calls."""
        with self._cache_lock:
            try:
                stat = self.path.stat()
                inode = int(stat.st_ino)
                size = int(stat.st_size)
            except OSError:
                inode = None
                size = 0

            if (
                self._active_keys_cache is None
                or inode != self._cache_inode
                or size < self._cache_offset
            ):
                self._active_keys_cache = {item.key for item in self.pending()}
                self._cache_inode = inode
                self._cache_offset = size
                return self._active_keys_cache

            events, next_offset = self.events_since(self._cache_offset)
            for event in events:
                key = str(event.get("key") or "")
                if not key:
                    continue
                if event.get("event") in {"queued", "requeued"}:
                    self._active_keys_cache.add(key)
                elif event.get("event") == "completed":
                    self._active_keys_cache.discard(key)
            self._cache_offset = next_offset
            return self._active_keys_cache

    def events_since(self, offset: int) -> tuple[list[dict[str, Any]], int]:
        """Read complete appended events after a byte offset.

        This is used by the long-lived verifier follower. It avoids replaying the
        complete append-only queue after every completed sandbox while preserving
        the same event semantics as ``pending()``.
        """
        if offset < 0:
            raise ValueError("offset must be >= 0")
        if not self.path.is_file():
            return [], offset
        with self.path.open("rb") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_SH)
            handle.seek(0, 2)
            size = handle.tell()
            if size < offset:
                offset = 0
            handle.seek(offset)
            payload = handle.read()
        complete_length = payload.rfind(b"\n") + 1
        if complete_length <= 0:
            return [], offset
        events: list[dict[str, Any]] = []
        consumed = offset
        for raw_line in payload[:complete_length].splitlines(keepends=True):
            consumed += len(raw_line)
            try:
                value = json.loads(raw_line.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            if isinstance(value, dict):
                events.append(value)
        return events, consumed

    def _append(self, event: str, key: str, **fields: Any) -> None:
        payload = {
            "schema_version": PENDING_SCHEMA_VERSION,
            "event": event,
            "key": key,
            "recorded_at": datetime.now(UTC).isoformat(),
            **fields,
        }
        append_text_locked(
            self.path,
            json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n",
        )


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


def _parse_datetime(value: object) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)
