from __future__ import annotations

import logging
from collections import Counter
from typing import Any

from .candidate_registration import CandidateRegistrar
from .candidate_verification import E2BCandidateVerifier
from .config import PipelineConfig
from .harbor_packaging import HarborPackager
from .pending_queue import PendingQueue
from .registry import JsonlRegistry
from .scoring import LanguageQuota
from .workspace import cloned_repository

LOGGER = logging.getLogger(__name__)


class PendingVerificationRunner:
    """Consume lightweight pending records with recoverable E2B verification."""

    def __init__(
        self,
        queue: PendingQueue,
        registry: JsonlRegistry,
        verifier: E2BCandidateVerifier,
    ) -> None:
        self.queue = queue
        self.registry = registry
        self.verifier = verifier

    @classmethod
    def from_config(cls, config: PipelineConfig) -> PendingVerificationRunner:
        registry = JsonlRegistry(config.candidates_path, config.rejections_path)
        quota = LanguageQuota(config.candidates_path)
        registrar = CandidateRegistrar(
            registry,
            quota,
            HarborPackager(config.e2b_api_key, config.catalog_dir),
        )
        return cls(
            PendingQueue(config.pending_path),
            registry,
            E2BCandidateVerifier(config, registry, registrar),
        )

    def run(
        self,
        *,
        max_items: int | None = None,
        max_consecutive_errors: int = 3,
    ) -> dict[str, int]:
        stats: Counter[str] = Counter()
        consecutive_errors = 0
        for item in self.queue.pending():
            if max_items is not None and stats["processed"] >= max_items:
                break
            stats["processed"] += 1
            candidate = item.candidate
            repo = dict(candidate["repo"])
            LOGGER.info("verifying pending candidate %s", repo["full_name"])
            outcome = self._verify_item(repo, candidate)
            stats[outcome] += 1
            if outcome == "error":
                self.queue.record_attempt(item.key)
                consecutive_errors += 1
                if consecutive_errors >= max_consecutive_errors:
                    stats["halted"] = 1
                    break
            else:
                self.queue.complete(item.key, outcome)
                consecutive_errors = 0
        stats["remaining"] = len(self.queue.pending())
        return dict(stats)

    def _verify_item(self, repo: dict[str, Any], candidate: dict[str, Any]) -> str:
        try:
            with cloned_repository(repo["full_name"], repo["base_commit"]) as repo_path:
                return self.verifier.verify(
                    repo,
                    repo_path,
                    score=dict(candidate["score"]),
                    direction=dict(candidate["direction"]),
                )
        except Exception as exc:
            LOGGER.exception("pending checkout failed for %s", repo.get("full_name"))
            self.registry.reject(
                repo,
                "pending_checkout",
                "stage_error",
                error_type=type(exc).__name__,
                error=str(exc)[:2_000],
            )
            return "error"
