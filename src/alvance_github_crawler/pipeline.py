from __future__ import annotations

import logging
from collections import Counter
from collections.abc import Iterable
from typing import Any

from .benchmark import E2BBenchmark, subset_test_command
from .build import DockerBuildVerifier
from .candidate_registration import CandidateRegistrar
from .config import PipelineConfig
from .direction import DirectionChecker, OpenAIDirectionJudge, PublicImplementationSearch
from .e2b_environment import (
    E2BEnvironmentManager,
    E2BOfflineVerifier,
    RepositoryTemplateBuildError,
    RuntimeTemplateBuildError,
    runtime_environment,
)
from .filters import HardFilter
from .github import GitHubClient
from .harbor_packaging import HarborPackager
from .registry import JsonlRegistry
from .scoring import LanguageQuota, SoftScorer
from .workspace import cloned_repository, tree_summary

LOGGER = logging.getLogger(__name__)


class Pipeline:
    def __init__(
        self,
        config: PipelineConfig,
        *,
        skip_e2b: bool = False,
        retry_rejected: bool = False,
    ) -> None:
        self.config = config
        self.skip_e2b = skip_e2b
        self.retry_rejected = retry_rejected
        self.github = GitHubClient(config.github_token)
        self.registry = JsonlRegistry(config.candidates_path, config.rejections_path)
        self.quota = LanguageQuota(config.candidates_path)
        self.hard_filter = HardFilter(self.github)
        self.soft_scorer = SoftScorer(self.github, self.quota)
        judge = OpenAIDirectionJudge(
            config.openai_api_key,
            config.openai_model,
            config.openai_base_url,
            timeout_s=config.openai_timeout_s,
            max_output_tokens=config.openai_max_output_tokens,
        )
        self.direction_checker = DirectionChecker(
            self.github,
            judge,
            PublicImplementationSearch(self.github),
            issue_limit=config.feature_issue_limit,
        )
        self.build_verifier = DockerBuildVerifier(timeout_s=config.build_timeout_s)
        self.e2b_environment = None if skip_e2b else E2BEnvironmentManager(config.e2b_api_key)
        self.e2b_offline = (
            None
            if skip_e2b
            else E2BOfflineVerifier(config.e2b_api_key, timeout_s=config.build_timeout_s)
        )
        self.benchmark = (
            None
            if skip_e2b
            else E2BBenchmark(
                config.e2b_api_key,
                runs=config.benchmark_runs,
                command_timeout_s=config.benchmark_timeout_s,
            )
        )
        self.harbor_packager = (
            None if skip_e2b else HarborPackager(config.e2b_api_key, config.catalog_dir)
        )
        self.registrar = CandidateRegistrar(
            self.registry,
            self.quota,
            self.harbor_packager,
        )

    def run(
        self,
        *,
        queries: Iterable[str] | None = None,
        max_repos: int | None = None,
    ) -> dict[str, int]:
        stats: Counter[str] = Counter()
        seen = self.registry.existing_repos()
        if not self.retry_rejected:
            seen |= self.registry.terminal_rejections()
        reached_limit = False
        for query in queries or self.config.queries:
            if reached_limit:
                break
            LOGGER.info("fetching candidates: %s", query)
            repos = self.github.search_repositories(
                query,
                pages=self.config.search_pages,
                per_page=self.config.max_candidates_per_query,
            )
            for repo in repos:
                full_name = repo.get("full_name", "unknown")
                if full_name in seen:
                    stats["duplicate"] += 1
                    continue
                if max_repos is not None and stats["processed"] >= max_repos:
                    reached_limit = True
                    break
                seen.add(full_name)
                stats["processed"] += 1
                LOGGER.info("processing %s", full_name)
                outcome = self._process_repo(repo)
                stats[outcome] += 1
        return dict(stats)

    def _process_repo(self, repo: dict[str, Any]) -> str:
        stage = "stage1_hard_filter"
        try:
            base_commit = self.github.get_head_sha(repo)
            repo["base_commit"] = base_commit
            tree = self.github.get_tree(repo["full_name"], base_commit)
            hard = self.hard_filter.evaluate(repo, tree)
            if not hard.ok:
                self.registry.reject(repo, stage, hard.reason)
                return "rejected"

            repo_size_kb = int(repo.get("size", 0) or 0)
            if repo_size_kb > self.config.max_repo_size_kb:
                self.registry.reject(
                    repo,
                    "stage2_soft_score",
                    "repo_too_large",
                    repo_size_kb=repo_size_kb,
                    max_repo_size_kb=self.config.max_repo_size_kb,
                )
                return "rejected"

            with cloned_repository(repo["full_name"], base_commit) as repo_path:
                stage = "stage2_soft_score"
                score = self.soft_scorer.evaluate(repo, tree, repo_path)
                if score.total < self.config.min_soft_score:
                    self.registry.reject(
                        repo,
                        stage,
                        f"score={score.total}",
                        score=score.to_dict(),
                    )
                    return "rejected"

                stage = "stage3_direction"
                summary = tree_summary(
                    repo_path,
                    max_entries=self.config.max_tree_entries,
                    max_chars=self.config.max_tree_chars,
                )
                direction = self.direction_checker.check(repo, summary)
                if direction is None:
                    self.registry.reject(repo, stage, "no_direction")
                    return "rejected"

                if self.skip_e2b:
                    stage = "stage4_local_docker_fallback"
                    build = self.build_verifier.verify(repo, base_commit, repo_path)
                    try:
                        if not build.ok:
                            self.registry.reject(
                                repo,
                                stage,
                                build.reason,
                                log_tail=build.log_tail,
                            )
                            return "rejected"

                        self.registrar.register(
                            repo,
                            score=score.to_dict(),
                            direction=direction.to_dict(),
                            build=build.to_dict(),
                            environment=None,
                            template_id=None,
                            benchmark=None,
                            adjusted_score=score.total,
                            status="offline_verified_local",
                        )
                        return "registered"
                    finally:
                        self.build_verifier.remove_image(build.image)

                assert self.e2b_environment is not None
                assert self.e2b_offline is not None
                assert self.benchmark is not None
                stage = "stage3_5_e2b_environment"
                try:
                    environment = self.e2b_environment.ensure(repo, repo_path, base_commit)
                except RuntimeTemplateBuildError as exc:
                    self.registry.reject(repo, stage, "infra_error", error=str(exc)[:2_000])
                    return "error"
                except RepositoryTemplateBuildError as exc:
                    self.registry.reject(repo, stage, "build_fail", error=str(exc)[:2_000])
                    return "rejected"

                runtime_env = runtime_environment(
                    (repo.get("language") or "").lower(),
                    environment.runtime_version,
                )
                stage = "stage4_e2b_offline_test"
                offline = self.e2b_offline.verify(
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
                        (repo.get("language") or "").lower(),
                        direction.target_paths,
                    )
                    if subset_cmd and subset_cmd != environment.test_cmd:
                        benchmark = self.benchmark.run(
                            environment.repository_template,
                            subset_cmd,
                            envs=runtime_env,
                        )

                adjusted_score = score.total
                status = "ready_for_phase1"
                if benchmark.flaky:
                    adjusted_score -= 2
                    status = "ready_for_phase1_flaky_test_suite"
                if not benchmark.resource_pass:
                    self.registry.reject(
                        repo,
                        stage,
                        "benchmark_resource_fail",
                        benchmark=benchmark.to_dict(),
                    )
                    return "rejected"
                if not benchmark.all_passed and not benchmark.flaky:
                    self.registry.reject(
                        repo,
                        stage,
                        "benchmark_test_fail",
                        benchmark=benchmark.to_dict(),
                    )
                    return "rejected"
                if adjusted_score < self.config.min_soft_score:
                    self.registry.reject(
                        repo,
                        stage,
                        f"flaky_adjusted_score={adjusted_score}",
                        benchmark=benchmark.to_dict(),
                    )
                    return "rejected"

                build_record = {
                    "ok": True,
                    "reason": "ok",
                    "image": "",
                    "dockerfile": "",
                    "test_cmd": environment.test_cmd,
                    "log_tail": "",
                }
                stage = "stage6_harbor_package"
                self.registrar.register(
                    repo,
                    score=score.to_dict(),
                    direction=direction.to_dict(),
                    build=build_record,
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
