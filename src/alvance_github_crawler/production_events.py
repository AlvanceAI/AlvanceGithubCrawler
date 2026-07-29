from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EVENT_SCHEMA_VERSION = "0.1"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class ProductionEventWriter:
    def __init__(self, path: Path | None) -> None:
        self.path = path

    def emit(
        self,
        *,
        stage: str,
        event_type: str,
        status: str,
        repo: str = "",
        reason: str = "",
        retryable: bool = False,
        **fields: Any,
    ) -> None:
        if self.path is None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": EVENT_SCHEMA_VERSION,
            "event_id": str(uuid.uuid4()),
            "occurred_at": utc_now(),
            "stage": stage,
            "event_type": event_type,
            "status": status,
            "repo": repo or None,
            "reason": reason or None,
            "retryable": retryable,
            **fields,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def read_events(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            events.append(payload)
    return events
