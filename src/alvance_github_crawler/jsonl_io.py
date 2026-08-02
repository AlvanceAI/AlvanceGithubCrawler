from __future__ import annotations

import fcntl
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def split_jsonl_lines(payload: str) -> list[str]:
    """Split JSONL only at its LF record delimiter.

    ``str.splitlines()`` also splits valid JSON string data such as U+2028.
    """
    return payload.split("\n")


def read_text_locked(path: Path) -> str:
    if not path.is_file():
        return ""
    with path.open("r", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_SH)
        return handle.read()


def append_text_locked(path: Path, payload: str, *, durable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        handle.write(payload)
        handle.flush()
        if durable:
            os.fsync(handle.fileno())


@dataclass(frozen=True, slots=True)
class JSONLReadBatch:
    """A complete, bounded batch read from an append-only JSONL file."""

    records: list[dict[str, Any]]
    inode: int
    next_offset: int
    file_size: int


class IncrementalJSONLReader:
    """Read newly appended JSONL records without rescanning the whole file.

    The cursor is committed by the caller only after the batch has been processed.
    If a worker is interrupted before ``commit``, that small batch is read again on
    the next run and the normal registry/queue identity checks make the replay safe.
    """

    def __init__(self, path: Path, cursor_path: Path) -> None:
        self.path = path
        self.cursor_path = cursor_path
        self.cursor_path.parent.mkdir(parents=True, exist_ok=True)
        self._inode, self._offset = self._load_cursor()

    @property
    def offset(self) -> int:
        return self._offset

    def read(self, max_records: int = 200) -> JSONLReadBatch:
        if max_records < 1:
            raise ValueError("max_records must be >= 1")
        try:
            stat = self.path.stat()
        except FileNotFoundError:
            return JSONLReadBatch([], self._inode or 0, self._offset, 0)

        inode = int(stat.st_ino)
        offset = self._offset
        if self._inode not in {None, 0, inode} or stat.st_size < offset:
            # A replacement or truncation means the old byte position is no longer
            # meaningful. The producer only appends, so replaying from zero is safe.
            offset = 0
            self._offset = 0

        with self.path.open("rb") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_SH)
            handle.seek(offset)
            payload = handle.read()

        if not payload:
            self._inode = inode
            return JSONLReadBatch([], inode, offset, int(stat.st_size))

        # Do not consume a line while the producer is still writing it.
        complete_length = payload.rfind(b"\n") + 1
        if complete_length <= 0:
            self._inode = inode
            return JSONLReadBatch([], inode, offset, int(stat.st_size))

        records: list[dict[str, Any]] = []
        consumed = offset
        for raw_line in payload[:complete_length].splitlines(keepends=True):
            consumed += len(raw_line)
            line = raw_line.rstrip(b"\r\n")
            if not line.strip():
                continue
            try:
                value = json.loads(line.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                # Invalid records are not useful to downstream stages, but advancing
                # past them prevents a malformed line from permanently blocking the
                # follower. The source producer validates its own output separately.
                continue
            if isinstance(value, dict):
                records.append(value)
            if len(records) >= max_records:
                break

        self._inode = inode
        return JSONLReadBatch(records, inode, consumed, int(stat.st_size))

    def commit(self, batch: JSONLReadBatch) -> None:
        if batch.next_offset < self._offset:
            raise ValueError("JSONL cursor cannot move backwards")
        self._inode = batch.inode
        self._offset = batch.next_offset
        payload = {
            "schema_version": "1",
            "source": str(self.path),
            "inode": self._inode,
            "offset": self._offset,
            "updated_at": time.time(),
        }
        temporary = self.cursor_path.with_suffix(self.cursor_path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temporary.replace(self.cursor_path)

    def _load_cursor(self) -> tuple[int | None, int]:
        try:
            value = json.loads(self.cursor_path.read_text(encoding="utf-8"))
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            return None, 0
        if not isinstance(value, dict):
            return None, 0
        try:
            inode = int(value.get("inode"))
            offset = max(0, int(value.get("offset", 0)))
        except (TypeError, ValueError):
            return None, 0
        return inode, offset
