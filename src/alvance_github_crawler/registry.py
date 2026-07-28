from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class JsonlRegistry:
    def __init__(self, candidates_path: Path, rejections_path: Path) -> None:
        self.candidates_path = candidates_path
        self.rejections_path = rejections_path
        candidates_path.parent.mkdir(parents=True, exist_ok=True)
        rejections_path.parent.mkdir(parents=True, exist_ok=True)

    def existing_repos(self) -> set[str]:
        if not self.candidates_path.is_file():
            return set()
        repos: set[str] = set()
        for line in self.candidates_path.read_text(encoding="utf-8").splitlines():
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
        for line in self.rejections_path.read_text(encoding="utf-8").splitlines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            repo = str(record.get("repo", ""))
            reason = str(record.get("reason", ""))
            if repo:
                latest[repo] = reason
        retryable = {"stage_error", "build_timeout"}
        return {repo for repo, reason in latest.items() if reason not in retryable}

    def register(self, record: dict[str, Any]) -> None:
        payload = {"registered_at": datetime.now(UTC).isoformat(), **record}
        self._append(self.candidates_path, payload)

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
        self._append(self.rejections_path, payload)

    @staticmethod
    def _append(path: Path, payload: dict[str, Any]) -> None:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
