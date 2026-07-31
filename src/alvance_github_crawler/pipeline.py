from __future__ import annotations

import json
import logging
import re
from collections import Counter
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from .catalog.harbor_packaging import HarborPackager
from .config import PipelineConfig
from .e2b.verification import E2BCandidateVerifier
from .github import GitHubClient, GitHubError
from .jsonl_io import read_text_locked
from .pending.queue import PendingQueue, build_pending_candidate
from .pending.registration import CandidateRegistrar
from .registry import JsonlRegistry
from .runtime.build import DockerBuildVerifier
from .screening.direction import DirectionChecker, OpenAIDirectionJudge, PublicImplementationSearch
from .screening.filters import HardFilter
from .screening.scoring import LanguageQuota, SoftScorer
from .workspace import cloned_repository, tree_summary

LOGGER = logging.getLogger(__name__)
COMMIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)


def catalog_repositories(catalog_dir: Path) -> set[str]:
    repositories: set[str] = set()
    for raw_line in read_text_locked(catalog_dir / "e2b-packages.jsonl").splitlines():
        try:
            package = json.loads(raw_line)
        except json.JSONDecodeError:
            continue
        repo = str(package.get("repo") or "") if isinstance(package, dict) else ""
        if repo:
            repositories.add(repo)
    return repositories


def load_crawl_candidates(
    path: Path,
    *,
    repositories: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    """Load validated, immutable candidates emitted by the `crawl` command."""
    if not path.is_file():
        raise ValueError(f"candidate input file does not exist: {path}")

    candidates: dict[str, dict[str, Any]] = {}
    for line_number, raw_line in enumerate(read_text_locked(path).splitlines(), 1):
        if not raw_line.strip():
            continue
        try:
            candidate = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON in {path}:{line_number}") from exc
        if not isinstance(candidate, dict):
            raise ValueError(f"candidate in {path}:{line_number} must be an object")

        full_name = str(candidate.get("repo") or "").strip()
        base_commit = str(candidate.get("base_commit") or "").strip()
        language = str(candidate.get("language") or "").lower()
        if not full_name or "/" not in full_name:
            raise ValueError(f"candidate in {path}:{line_number} has no valid repo")
        if not COMMIT_SHA_RE.fullmatch(base_commit):
            raise ValueError(
                f"candidate {full_name} in {path}:{line_number} has no full commit SHA"
            )
        if not language:
            raise ValueError(f"candidate {full_name} in {path}:{line_number} has no language")
        if full_name in candidates:
            raise ValueError(f"duplicate candidate repo in {path}: {full_name}")
        candidates[full_name] = candidate

    if repositories is None:
        return list(candidates.values())

    selected: list[dict[str, Any]] = []
    selected_names: set[str] = set()
    for raw_name in repositories:
        full_name = raw_name.strip()
        if not full_name:
            continue
        if full_name in selected_names:
            raise ValueError(f"duplicate --repository value: {full_name}")
        try:
            selected.append(candidates[full_name])
        except KeyError as exc:
            raise ValueError(f"repository is not present in candidate input: {full_name}") from exc
        selected_names.add(full_name)
    return selected


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
        self.github = GitHubClient(config.github_tokens)
        self.registry = JsonlRegistry(
            config.candidates_path,
            config.rejections_path,
            config.output_dir / "events.jsonl",
        )
        self.quota = LanguageQuota(config.candidates_path)
        self.hard_filter = HardFilter(self.github)
        self.soft_scorer = SoftScorer(
            self.github,
            self.quota,
            enforce_language_quota=config.language_quota_enabled,
        )
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
            else HarborPackager(
                config.e2b_api_key,
                config.catalog_dir,
                cpu_count=config.e2b_cpu_count,
                memory_mb=config.e2b_memory_mb,
            )
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
        seen |= catalog_repositories(self.config.catalog_dir)
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

    def run_crawl_candidates(
        self,
        path: Path,
        *,
        max_repos: int | None = None,
        repositories: Iterable[str] | None = None,
    ) -> dict[str, int]:
        """Process exact commits from a prior `crawl` JSONL output.

        The crawl record remains the provenance source for immutable candidate fields.
        A lightweight repository API lookup is only used for data not included in that
        record, notably the reported repository size used by Stage 2.
        """
        candidates = load_crawl_candidates(path, repositories=repositories)
        stats: Counter[str] = Counter(input_total=len(candidates))
        seen = self.registry.existing_repos()
        seen |= self.pending.known_repos()
        seen |= catalog_repositories(self.config.catalog_dir)
        if not self.retry_rejected:
            seen |= self.registry.terminal_rejections()

        selected: list[dict[str, Any]] = []
        for candidate in candidates:
            full_name = str(candidate["repo"])
            if full_name in seen:
                stats["duplicate"] += 1
                continue
            if max_repos is not None and len(selected) >= max_repos:
                break
            seen.add(full_name)
            selected.append(candidate)

        stats["processed"] = len(selected)
        if self.config.prescreen_concurrency == 1:
            outcomes = map(self._process_crawl_candidate, selected)
            for outcome in outcomes:
                stats[outcome] += 1
        else:
            with ThreadPoolExecutor(
                max_workers=self.config.prescreen_concurrency,
                thread_name_prefix="prescreen",
            ) as pool:
                for outcome in pool.map(self._process_crawl_candidate, selected):
                    stats[outcome] += 1
        return dict(stats)

    def _process_crawl_candidate(self, candidate: dict[str, Any]) -> str:
        full_name = str(candidate["repo"])
        LOGGER.info("processing crawled candidate %s@%s", full_name, candidate["base_commit"])
        try:
            repo = self._repository_from_crawl_candidate(candidate)
        except ValueError as exc:
            self.registry.reject(
                {"full_name": full_name},
                "candidate_input",
                "invalid_candidate",
                error=str(exc)[:2_000],
            )
            return "rejected"
        except Exception as exc:
            LOGGER.exception("could not hydrate crawled candidate %s", full_name)
            self.registry.reject(
                {"full_name": full_name},
                "candidate_input",
                "stage_error",
                error_type=type(exc).__name__,
                error=str(exc)[:2_000],
            )
            return "error"
        return self._process_repo(repo)

    def _repository_from_crawl_candidate(self, candidate: dict[str, Any]) -> dict[str, Any]:
        """Combine a crawl record with current non-provenance repository metadata."""
        full_name = str(candidate["repo"])
        base_commit = str(candidate["base_commit"])
        repo = self.github.get_repository(full_name)
        source_tree = self.github.get_commit_tree(full_name, base_commit)
        expected_tree = str(candidate.get("source_tree") or "")
        if expected_tree and source_tree != expected_tree:
            raise ValueError(
                f"source tree mismatch for {full_name}@{base_commit}: "
                f"expected {expected_tree}, got {source_tree}"
            )

        # Keep eligibility and provenance tied to the original crawl snapshot rather
        # than allowing a later default-branch update to silently change the task.
        repo.update(
            {
                "full_name": full_name,
                "html_url": str(candidate.get("html_url") or repo.get("html_url") or ""),
                "name": full_name.rsplit("/", 1)[-1],
                "language": str(candidate.get("language") or repo.get("language") or ""),
                "stargazers_count": int(candidate.get("stars") or 0),
                "license": {"spdx_id": str(candidate.get("license") or "NOASSERTION")},
                "description": str(candidate.get("description") or ""),
                "topics": list(candidate.get("topics") or []),
                "default_branch": str(candidate.get("default_branch") or "main"),
                "pushed_at": str(candidate.get("pushed_at") or ""),
                "fork": bool(candidate.get("fork", False)),
                "archived": bool(candidate.get("archived", False)),
                "mirror_url": "https://mirror.invalid" if candidate.get("mirror") else None,
                "base_commit": base_commit,
                "source_tree": source_tree,
                "crawl_time": str(candidate.get("crawl_time") or ""),
                "crawl_test_evidence": list(candidate.get("test_evidence") or []),
            }
        )
        return repo

    def _process_repo(self, repo: dict[str, Any]) -> str:
        stage = "stage1_hard_filter"
        try:
            base_commit = str(repo.get("base_commit") or "")
            if not base_commit:
                base_commit = self.github.get_head_sha(repo)
                repo["base_commit"] = base_commit
            elif not repo.get("source_tree"):
                repo["source_tree"] = self.github.get_commit_tree(repo["full_name"], base_commit)
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
