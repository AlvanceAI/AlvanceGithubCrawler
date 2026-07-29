from __future__ import annotations

import re
from collections import deque
from dataclasses import dataclass, field
from typing import Any

ANSI_ESCAPE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
URL_CREDENTIALS = re.compile(r"(https?://)[^/@\s]+@")
SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(api[_-]?key|authorization|password|token)\s*([=:])\s*([^\s]+)"
)


@dataclass(slots=True)
class E2BBuildLogBuffer:
    """Keep a bounded, sanitized tail of E2B template build messages."""

    max_lines: int = 80
    max_line_chars: int = 1_000
    _lines: deque[str] = field(init=False)

    def __post_init__(self) -> None:
        self._lines = deque(maxlen=self.max_lines)

    def __call__(self, entry: Any) -> None:
        message = str(getattr(entry, "message", "") or "")
        for line in message.splitlines():
            sanitized = sanitize_build_log_line(line)
            if sanitized:
                self._lines.append(sanitized[-self.max_line_chars :])

    def tail(self, max_chars: int = 8_000) -> str:
        return "\n".join(self._lines)[-max_chars:]

    def error_message(self, error: Exception) -> str:
        tail = self.tail()
        if not tail:
            return str(error)
        return f"{error}\nbuild log tail:\n{tail}"


def sanitize_build_log_line(line: str) -> str:
    line = ANSI_ESCAPE.sub("", line)
    line = URL_CREDENTIALS.sub(r"\1[REDACTED]@", line)
    return SECRET_ASSIGNMENT.sub(r"\1\2[REDACTED]", line).strip()
