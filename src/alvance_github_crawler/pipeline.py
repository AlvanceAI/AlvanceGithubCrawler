from __future__ import annotations

import logging
from collections import Counter
from collections.abc import Iterable
from typing import Any

from .runtime.build import DockerBuildVerifier
from .pending.registration import CandidateRegistrar
from .e2b.verification import E2BCandidateVerifier
from .config import PipelineConfig
from .screening.direction import DirectionChecker, OpenAIDirectionJudge, PublicImplementationSearch
from .screening.filters import HardFilter
from .github import GitHubClient, GitHubError
from .catalog.harbor_packaging import HarborPackager
from .pending.queue import PendingQueue, build_pending_candidate
from .registry import JsonlRegistry
from .screening.scoring import LanguageQuota, SoftScorer
from .workspace import cloned_repository, tree_summary

LOGGER = logging.getLogger(__name__)


class Pipeline:
    def __init__(
        self,
        config: PipelineConfig,
        *,
        skip_e2b: bool = False,
        defer_e2b: bool = False,
        retry_rejected: bool = False,
    ) -> None:
        self.config = config
        self.skip_e2b = skip_e2b
        self.defer_e2b = defer_e2b
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
        self.pending = PendingQueue(config.pending_path)
        registered_repos = self.registry.existing_repos()
        for pending in self.pending.pending():
            repo = pending.candidate.get("repo") or {}
            if str(repo.get("full_name") or "") in registered_repos:
                # Registered-but-not-completed leftovers are already counted
                # from candidates.jsonl by LanguageQuota.
                continue
            language = str(repo.get("language") or "").lower()
            if language:
                self.quota.register(language)
        self.harbor_packager = (
            None
            if skip_e2b or defer_e2b
            else HarborPackager(config.e2b_api_key, config.catalog_dir)
        )
        self.registrar = CandidateRegistrar(
            self.registry,
            self.quota,
            self.harbor_packager,
        )
        self.e2b_verifier = (
            None
            if skip_e2b or defer_e2b
            else E2BCandidateVerifier(config, self.registry, self.registrar)
        )

    def run(
        self,
        *,
        queries: Iterable[str] | None = None,
        max_repos: int | None = None,
    ) -> dict[str, int]:
        stats: Counter[str] = Counter()
        seen = self.registry.existing_repos()
        seen |= self.pending.active_repos()
        if not self.retry_rejected:
            seen |= self.registry.terminal_rejections()
        reached_limit = False
        for query in queries or self.config.queries:
            if reached_limit:
                break
            LOGGER.info("fetching candidates: %s", query)
            try:
                repos = self.github.search_repositories(
                    query,
                    pages=self.config.search_pages,
                    per_page=self.config.max_candidates_per_query,
                )
            except GitHubError:
                LOGGER.exception("repository search failed: %s", query)
                stats["search_error"] += 1
                continue
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

            stage = "stage2_checkout"
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

                if self.defer_e2b:
                    candidate = build_pending_candidate(
                        repo,
                        score.to_dict(),
                        direction.to_dict(),
                    )
                    if not self.pending.enqueue(candidate):
                        return "duplicate"
                    self.quota.register(str(repo.get("language") or ""))
                    return "queued"

                assert self.e2b_verifier is not None
                return self.e2b_verifier.verify(
                    repo,
                    repo_path,
                    score=score.to_dict(),
                    direction=direction.to_dict(),
                )
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
