from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from ..config import PipelineConfig
from ..pending.registration import CandidateRegistrar
from ..registry import JsonlRegistry
from ..runtime.profiles import UnsupportedRuntimeError
from . import (
    E2BEnvironmentManager,
    E2BOfflineVerifier,
    RepositoryTemplateBuildError,
    RuntimeTemplateBuildError,
    runtime_environment,
)
from .benchmark import E2BBenchmark, subset_test_command

LOGGER = logging.getLogger(__name__)


class E2BCandidateVerifier:
    """Build and validate one pre-screened candidate entirely in E2B."""

    def __init__(
        self,
        config: PipelineConfig,
        registry: JsonlRegistry,
        registrar: CandidateRegistrar,
    ) -> None:
        self.config = config
        self.registry = registry
        self.registrar = registrar
        self.environment = E2BEnvironmentManager(
            config.e2b_api_key,
            cpu_count=config.e2b_cpu_count,
            memory_mb=config.e2b_memory_mb,
        )
        self.offline = E2BOfflineVerifier(
            config.e2b_api_key,
            timeout_s=config.build_timeout_s,
        )
        self.benchmark = E2BBenchmark(
            config.e2b_api_key,
            runs=config.benchmark_runs,
            command_timeout_s=config.benchmark_timeout_s,
        )

    def verify(
        self,
        repo: dict[str, Any],
        repo_path: Path,
        *,
        score: dict[str, Any],
        direction: dict[str, Any],
    ) -> str:
        stage = "stage3_5_e2b_environment"
        try:
            try:
                environment = self.environment.ensure(repo, repo_path, str(repo["base_commit"]))
            except RuntimeTemplateBuildError as exc:
                if is_e2b_key_exhausted_error(exc):
                    self.registry.reject(
                        repo,
                        stage,
                        "e2b_key_exhausted",
                        error=str(exc)[-4_000:],
                    )
                    return "key_exhausted"
                if is_resource_e2b_error(exc):
                    self.registry.reject(
                        repo,
                        stage,
                        "e2b_resource_exhausted",
                        error=str(exc)[-4_000:],
                    )
                    return "rejected"
                self.registry.reject(repo, stage, "infra_error", error=str(exc)[-4_000:])
                return "error"
            except RepositoryTemplateBuildError as exc:
                if is_e2b_key_exhausted_error(exc):
                    self.registry.reject(
                        repo,
                        stage,
                        "e2b_key_exhausted",
                        error=str(exc)[-4_000:],
                    )
                    return "key_exhausted"
                if is_resource_e2b_error(exc):
                    self.registry.reject(
                        repo,
                        stage,
                        "e2b_resource_exhausted",
                        error=str(exc)[-4_000:],
                    )
                    return "rejected"
                if is_transient_e2b_error(exc):
                    self.registry.reject(repo, stage, "infra_error", error=str(exc)[-4_000:])
                    return "error"
                self.registry.reject(repo, stage, "build_fail", error=str(exc)[-4_000:])
                return "rejected"

            runtime_env = runtime_environment(
                str(repo.get("language") or "").lower(),
                environment.runtime_version,
            )
            stage = "stage4_e2b_offline_test"
            offline = self.offline.verify(
                environment.repository_template,
                environment.test_cmd,
                envs=runtime_env,
                user=environment.execution_user,
            )
            if not offline.ok:
                offline_reason = (
                    "e2b_resource_exhausted"
                    if is_resource_e2b_error(
                        RuntimeError(
                            f"exit_code={offline.exit_code}\n"
                            f"{offline.stdout_tail}\n{offline.stderr_tail}"
                        )
                    )
                    else offline.reason
                )
                self.registry.reject(
                    repo,
                    stage,
                    offline_reason,
                    offline=offline.to_dict(),
                    environment=environment.to_dict(),
                )
                return "rejected"

            stage = "stage5_e2b_benchmark"
            benchmark = self.benchmark.run(
                environment.repository_template,
                environment.test_cmd,
                envs=runtime_env,
                user=environment.execution_user,
            )
            if not benchmark.resource_pass:
                subset_cmd = subset_test_command(
                    repo_path,
                    str(repo.get("language") or "").lower(),
                    list(direction.get("target_paths") or []),
                )
                if subset_cmd and subset_cmd != environment.test_cmd:
                    benchmark = self.benchmark.run(
                        environment.repository_template,
                        subset_cmd,
                        envs=runtime_env,
                        user=environment.execution_user,
                    )

            adjusted_score = float(score["total"])
            status = "ready_for_phase1"
            if benchmark.flaky:
                adjusted_score -= 2
                status = "ready_for_phase1_flaky_test_suite"
            rejection = benchmark_rejection(
                benchmark,
                adjusted_score=adjusted_score,
                minimum_score=self.config.min_soft_score,
            )
            if rejection:
                self.registry.reject(
                    repo,
                    stage,
                    rejection,
                    benchmark=benchmark.to_dict(),
                )
                return "rejected"

            stage = "stage6_harbor_package"
            self.registrar.register(
                repo,
                score=score,
                direction=direction,
                build={
                    "ok": True,
                    "reason": "ok",
                    "image": "",
                    "dockerfile": "",
                    "test_cmd": environment.test_cmd,
                    "log_tail": "",
                },
                environment={**environment.to_dict(), "offline": offline.to_dict()},
                template_id=environment.repository_template,
                benchmark=benchmark.to_dict(),
                adjusted_score=adjusted_score,
                status=status,
            )
            return "registered"
        except Exception as exc:
            if isinstance(exc, UnsupportedRuntimeError):
                self.registry.reject(
                    repo,
                    stage,
                    "unsupported_runtime",
                    error=str(exc)[-4_000:],
                )
                return "rejected"
            if is_e2b_key_exhausted_error(exc):
                LOGGER.error("%s exhausted its E2B key during %s", repo.get("full_name"), stage)
                self.registry.reject(
                    repo,
                    stage,
                    "e2b_key_exhausted",
                    error_type=type(exc).__name__,
                    error=str(exc)[-4_000:],
                )
                return "key_exhausted"
            LOGGER.exception("%s failed during %s", repo.get("full_name"), stage)
            self.registry.reject(
                repo,
                stage,
                "stage_error",
                error_type=type(exc).__name__,
                error=str(exc)[:2_000],
            )
            return "error"


def benchmark_rejection(
    benchmark: Any,
    *,
    adjusted_score: float,
    minimum_score: float,
) -> str:
    if not benchmark.resource_pass:
        return "benchmark_resource_fail"
    if not benchmark.all_passed and not benchmark.flaky:
        return "benchmark_test_fail"
    if adjusted_score < minimum_score:
        return f"flaky_adjusted_score={adjusted_score}"
    return ""


def is_transient_e2b_error(error: BaseException) -> bool:
    message = str(error).lower()
    markers = (
        "429",
        "rate limit",
        "too many",
        "concurrent",
        "temporarily unavailable",
        "service unavailable",
        "bad gateway",
        "gateway timeout",
        "connection error",
        "connection reset",
        "connection timed out",
        "request timeout",
        "request timed out",
        "internal server error",
    )
    return any(marker in message for marker in markers)


def is_e2b_key_exhausted_error(error: BaseException) -> bool:
    message = str(error).lower()
    markers = (
        "insufficient credits",
        "not enough credits",
        "no credits remaining",
        "credits exhausted",
        "credit limit reached",
        "monthly credit limit",
        "spending limit reached",
        "payment required",
        "http 402",
        "status code 402",
        "status_code=402",
    )
    return any(marker in message for marker in markers)


def is_resource_e2b_error(error: BaseException) -> bool:
    message = str(error).lower()
    markers = (
        "signal: killed",
        "signal: 9",
        "sigkill",
        "out of memory",
        "oom killed",
        "oom-kill",
        "cannot allocate memory",
        "memory limit",
        "exit code 137",
        "exit_code=137",
    )
    return any(marker in message for marker in markers)
