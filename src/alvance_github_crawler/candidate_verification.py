from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from .benchmark import E2BBenchmark, subset_test_command
from .candidate_registration import CandidateRegistrar
from .config import PipelineConfig
from .e2b_environment import (
    E2BEnvironmentManager,
    E2BOfflineVerifier,
    RepositoryTemplateBuildError,
    RuntimeTemplateBuildError,
    runtime_environment,
)
from .registry import JsonlRegistry

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
        self.environment = E2BEnvironmentManager(config.e2b_api_key)
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
                self.registry.reject(repo, stage, "infra_error", error=str(exc)[:2_000])
                return "error"
            except RepositoryTemplateBuildError as exc:
                self.registry.reject(repo, stage, "build_fail", error=str(exc)[:2_000])
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
            )
            if not offline.ok:
                self.registry.reject(
                    repo,
                    stage,
                    offline.reason,
                    offline=offline.to_dict(),
                    environment=environment.to_dict(),
                )
                return "rejected"

            stage = "stage5_e2b_benchmark"
            benchmark = self.benchmark.run(
                environment.repository_template,
                environment.test_cmd,
                envs=runtime_env,
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
