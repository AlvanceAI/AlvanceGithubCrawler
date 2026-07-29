from __future__ import annotations

from types import SimpleNamespace

from alvance_github_crawler.e2b.build_logs import E2BBuildLogBuffer


def test_build_log_buffer_is_bounded_and_sanitized() -> None:
    logs = E2BBuildLogBuffer(max_lines=2)
    logs(SimpleNamespace(message="old line"))
    logs(SimpleNamespace(message="https://secret@example.com/simple"))
    logs(SimpleNamespace(message="API_KEY=super-secret"))

    assert logs.tail() == "https://[REDACTED]@example.com/simple\nAPI_KEY=[REDACTED]"
    assert "old line" not in logs.error_message(RuntimeError("failed"))


def test_build_log_buffer_handles_entries_without_messages() -> None:
    logs = E2BBuildLogBuffer()
    logs(object())

    assert logs.error_message(RuntimeError("failed")) == "failed"
