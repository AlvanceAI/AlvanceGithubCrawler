from __future__ import annotations

import json
import threading
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .jsonl_io import append_text_locked, read_text_locked
from .production_events import ProductionEventWriter

RETRYABLE_REJECTION_REASONS = {
    "stage_error",
    "build_timeout",
    "runtime_prep_timeout",
    "runtime_prep_fail",
    "infra_error",
    "e2b_key_exhausted",
}


class JsonlRegistry:
    def __init__(
        self,
        candidates_path: Path,
        rejections_path: Path,
        events_path: Path | None = None,
    ) -> None:
        self.candidates_path = candidates_path
        self.rejections_path = rejections_path
        candidates_path.parent.mkdir(parents=True, exist_ok=True)
        rejections_path.parent.mkdir(parents=True, exist_ok=True)
        self.events = ProductionEventWriter(events_path)
        self._write_lock = threading.Lock()

    def existing_repos(self) -> set[str]:
        if not self.candidates_path.is_file():
            return set()
        repos: set[str] = set()
        for line in read_text_locked(self.candidates_path).splitlines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("repo"):
                repos.add(str(record["repo"]))
        return repos

    def terminal_rejections(self) -> set[str]:
        """Skip deterministic rejections while allowing transient stage errors to retry."""
        if not self.rejections_path.is_file():
            return set()
        latest: dict[str, str] = {}
        for line in read_text_locked(self.rejections_path).splitlines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            repo = str(record.get("repo", ""))
            reason = str(record.get("reason", ""))
            if repo:
                latest[repo] = reason
        return {
            repo
            for repo, reason in latest.items()
            if reason not in RETRYABLE_REJECTION_REASONS
        }

    def register(self, record: dict[str, Any]) -> None:
        payload = {"registered_at": datetime.now(UTC).isoformat(), **record}
        with self._write_lock:
            self._append(self.candidates_path, payload)
            self.events.emit(
                stage="registry",
                event_type="candidate_registered",
                status="ok",
                repo=str(payload.get("repo") or ""),
                candidate_status=str(payload.get("status") or ""),
            )

    def reject(
        self,
        repo: dict[str, Any],
        stage: str,
        reason: str,
        **details: Any,
    ) -> None:
        payload = {
            "rejected_at": datetime.now(UTC).isoformat(),
            "repo": repo.get("full_name", "unknown"),
            "stage": stage,
            "reason": reason,
            **details,
        }
        with self._write_lock:
            self._append(self.rejections_path, payload)
            self.events.emit(
                stage=stage,
                event_type="candidate_rejected",
                status="rejected",
                repo=str(payload.get("repo") or ""),
                reason=reason,
                retryable=reason in RETRYABLE_REJECTION_REASONS,
            )

    @staticmethod
    def _append(path: Path, payload: dict[str, Any]) -> None:
        append_text_locked(path, json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
