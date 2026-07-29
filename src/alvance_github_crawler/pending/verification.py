from __future__ import annotations

import logging
from collections import Counter
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from typing import Any

from ..catalog.harbor_packaging import HarborPackager
from ..config import PipelineConfig
from ..e2b.verification import E2BCandidateVerifier
from ..registry import JsonlRegistry
from ..screening.scoring import LanguageQuota
from ..workspace import cloned_repository
from .queue import PendingQueue
from .registration import CandidateRegistrar

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
            HarborPackager(
                config.e2b_api_key,
                config.catalog_dir,
                cpu_count=config.e2b_cpu_count,
                memory_mb=config.e2b_memory_mb,
            ),
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
        max_attempts_per_item: int = 3,
        max_workers: int = 1,
    ) -> dict[str, int]:
        if max_workers < 1:
            raise ValueError("max_workers must be >= 1")
        if max_attempts_per_item < 1:
            raise ValueError("max_attempts_per_item must be >= 1")
        stats: Counter[str] = Counter()
        consecutive_errors = 0
        registered = self.registry.existing_repos()
        attempts = self.queue.attempt_counts()
        items = []
        for item in self.queue.pending():
            candidate = item.candidate
            repo = dict(candidate["repo"])
            if str(repo.get("full_name") or "") in registered:
                # Crash between register and complete leaves the item active;
                # never re-verify or re-register an already-registered repo.
                self.queue.complete(item.key, "already_registered")
                stats["already_registered"] += 1
                continue
            if max_items is not None and len(items) >= max_items:
                break
            items.append(item)

        with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="e2b-verify") as pool:
            item_iterator = iter(items)
            futures: dict[Future[str], Any] = {}
            halted = False

            def submit_next() -> bool:
                try:
                    item = next(item_iterator)
                except StopIteration:
                    return False
                candidate = item.candidate
                repo = dict(candidate["repo"])
                LOGGER.info("verifying pending candidate %s", repo["full_name"])
                future = pool.submit(self._verify_item, repo, candidate)
                futures[future] = item
                return True

            while len(futures) < max_workers and submit_next():
                pass

            while futures:
                completed, _ = wait(futures, return_when=FIRST_COMPLETED)
                for future in completed:
                    item = futures.pop(future)
                    outcome = future.result()
                    stats["processed"] += 1
                    stats[outcome] += 1
                    repo_name = str((item.candidate.get("repo") or {}).get("full_name") or item.key)
                    LOGGER.info(
                        "pending candidate %s finished outcome=%s processed=%d in_flight=%d",
                        repo_name,
                        outcome,
                        stats["processed"],
                        len(futures),
                    )
                    if outcome == "error":
                        self.queue.record_attempt(item.key)
                        consecutive_errors += 1
                        if attempts.get(item.key, 0) + 1 >= max_attempts_per_item:
                            # The rejection is already recorded; remove permanently
                            # broken items so they cannot block later queue entries.
                            self.queue.complete(item.key, "error_exhausted")
                            stats["exhausted"] += 1
                        else:
                            self.queue.defer(item.key)
                    else:
                        self.queue.complete(item.key, outcome)
                        consecutive_errors = 0

                    if consecutive_errors >= max_consecutive_errors and not halted:
                        halted = True
                        stats["halted"] = 1

                if halted:
                    continue
                while len(futures) < max_workers and submit_next():
                    pass
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
