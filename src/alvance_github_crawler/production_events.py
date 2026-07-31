from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .jsonl_io import append_text_locked, read_text_locked

EVENT_SCHEMA_VERSION = "0.1"


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


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
        append_text_locked(
            self.path,
            json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n",
        )


def read_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in read_text_locked(path).splitlines():
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            events.append(payload)
    return events
