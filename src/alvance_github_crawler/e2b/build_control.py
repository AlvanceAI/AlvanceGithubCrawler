from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any


class E2BTemplateBuildTimeout(TimeoutError):
    pass


def build_template_with_timeout(
    Template: Any,
    builder: Any,
    *,
    name: str,
    cpu_count: int,
    memory_mb: int,
    api_key: str,
    timeout_s: int,
    skip_cache: bool = False,
    on_build_logs: Callable[[Any], None] | None = None,
    poll_interval_s: float = 1.0,
) -> Any:
    """Build an E2B template without allowing status polling to run forever."""
    if timeout_s < 1:
        raise ValueError("template build timeout must be positive")

    deadline = time.monotonic() + timeout_s
    request_timeout = min(60.0, float(timeout_s))
    info = Template.build_in_background(
        builder,
        name=name,
        cpu_count=cpu_count,
        memory_mb=memory_mb,
        skip_cache=skip_cache,
        api_key=api_key,
        request_timeout=request_timeout,
        on_build_logs=on_build_logs,
    )
    logs_offset = 0

    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise _timeout_error(info, name, timeout_s)

        status = Template.get_build_status(
            info,
            logs_offset=logs_offset,
            api_key=api_key,
            request_timeout=min(request_timeout, max(1.0, remaining)),
        )
        entries = list(getattr(status, "log_entries", ()) or ())
        logs_offset += len(entries)
        if on_build_logs is not None:
            for entry in entries:
                on_build_logs(entry)

        raw_status = getattr(status, "status", "")
        state = str(getattr(raw_status, "value", raw_status)).lower()
        if state == "ready":
            return info
        if state == "error":
            reason = getattr(status, "reason", None)
            message = str(getattr(reason, "message", "") or "E2B template build failed")
            raise RuntimeError(message)
        if state not in {"building", "waiting"}:
            raise RuntimeError(f"unknown E2B template build status: {state or 'missing'}")

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise _timeout_error(info, name, timeout_s)
        time.sleep(min(poll_interval_s, remaining))


def _timeout_error(info: Any, name: str, timeout_s: int) -> E2BTemplateBuildTimeout:
    template_id = str(getattr(info, "template_id", "unknown"))
    build_id = str(getattr(info, "build_id", "unknown"))
    return E2BTemplateBuildTimeout(
        f"E2B template build timed out after {timeout_s}s: "
        f"name={name} template_id={template_id} build_id={build_id}"
    )
