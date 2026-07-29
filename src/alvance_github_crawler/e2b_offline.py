from __future__ import annotations

import time
from dataclasses import asdict, dataclass
from typing import Any

from .runtime_profiles import command_with_environment


@dataclass(slots=True)
class OfflineTestResult:
    ok: bool
    reason: str
    duration_s: float
    exit_code: int
    stdout_tail: str = ""
    stderr_tail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class E2BOfflineVerifier:
    def __init__(self, api_key: str, *, timeout_s: int = 600) -> None:
        self.api_key = api_key
        self.timeout_s = timeout_s

    def verify(
        self,
        template: str,
        test_cmd: str,
        *,
        envs: dict[str, str] | None = None,
        user: str = "root",
    ) -> OfflineTestResult:
        try:
            from e2b import Sandbox
        except ImportError as exc:
            raise RuntimeError("e2b SDK is not installed; install the project with [e2b]") from exc

        started = time.monotonic()
        with Sandbox.create(
            template=template,
            allow_internet_access=False,
            timeout=self.timeout_s + 60,
            envs=envs,
            api_key=self.api_key,
        ) as sandbox:
            try:
                result = sandbox.commands.run(
                    command_with_environment(test_cmd, envs),
                    user=user,
                    timeout=self.timeout_s,
                )
            except Exception as exc:
                if hasattr(exc, "exit_code"):
                    result = exc
                elif type(exc).__name__ == "TimeoutException":
                    return OfflineTestResult(
                        ok=False,
                        reason="offline_test_timeout",
                        duration_s=round(time.monotonic() - started, 2),
                        exit_code=-1,
                        stderr_tail=str(exc)[-4_000:],
                    )
                else:
                    raise
        return OfflineTestResult(
            ok=result.exit_code == 0,
            reason="ok" if result.exit_code == 0 else "offline_test_fail",
            duration_s=round(time.monotonic() - started, 2),
            exit_code=result.exit_code,
            stdout_tail=(getattr(result, "stdout", "") or "")[-4_000:],
            stderr_tail=(getattr(result, "stderr", "") or "")[-4_000:],
        )
