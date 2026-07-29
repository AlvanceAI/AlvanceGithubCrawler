from __future__ import annotations

import logging
from collections import Counter, deque
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import replace
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
        verifier: E2BCandidateVerifier | None,
        *,
        verifiers: tuple[E2BCandidateVerifier, ...] | None = None,
    ) -> None:
        self.queue = queue
        self.registry = registry
        self.verifier = verifier
        self.verifiers = verifiers or (verifier,)

    @classmethod
    def from_config(cls, config: PipelineConfig) -> PendingVerificationRunner:
        if not config.e2b_api_keys:
            raise ValueError("at least one E2B API key is required")
        registry = JsonlRegistry(config.candidates_path, config.rejections_path)
        quota = LanguageQuota(config.candidates_path)
        verifiers: list[E2BCandidateVerifier] = []
        for api_key in config.e2b_api_keys:
            per_key_config = replace(
                config,
                e2b_api_key=api_key,
                e2b_api_keys=(api_key,),
            )
            registrar = CandidateRegistrar(
                registry,
                quota,
                HarborPackager(
                    api_key,
                    config.catalog_dir,
                    cpu_count=config.e2b_cpu_count,
                    memory_mb=config.e2b_memory_mb,
                ),
            )
            verifiers.append(E2BCandidateVerifier(per_key_config, registry, registrar))
        return cls(
            PendingQueue(config.pending_path),
            registry,
            verifiers[0],
            verifiers=tuple(verifiers),
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
        registered = self.registry.existing_repos()
        attempts = self.queue.attempt_counts()
        items: deque[Any] = deque()
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
        scheduled_keys = {item.key for item in items}

        lane_count = len(self.verifiers)
        total_workers = max_workers * lane_count
        consecutive_errors = [0] * lane_count
        in_flight = [0] * lane_count
        halted_lanes: set[int] = set()
        exhausted_lanes: set[int] = set()

        with ThreadPoolExecutor(
            max_workers=total_workers,
            thread_name_prefix="e2b-verify",
        ) as pool:
            futures: dict[Future[str], tuple[Any, int]] = {}

            def refresh_items() -> None:
                if max_items is not None:
                    return
                for pending_item in self.queue.pending():
                    if pending_item.key in scheduled_keys:
                        continue
                    scheduled_keys.add(pending_item.key)
                    items.append(pending_item)

            def submit_next(lane: int) -> bool:
                if not items or lane in halted_lanes or lane in exhausted_lanes:
                    return False
                item = items.popleft()
                candidate = item.candidate
                repo = dict(candidate["repo"])
                LOGGER.info(
                    "verifying pending candidate %s key_slot=%d",
                    repo["full_name"],
                    lane + 1,
                )
                future = pool.submit(self._verify_for_lane, lane, repo, candidate)
                futures[future] = (item, lane)
                in_flight[lane] += 1
                return True

            for lane in range(lane_count):
                while in_flight[lane] < max_workers and submit_next(lane):
                    pass

            while futures:
                completed, _ = wait(futures, return_when=FIRST_COMPLETED)
                for future in completed:
                    item, lane = futures.pop(future)
                    in_flight[lane] -= 1
                    outcome = future.result()
                    stats["processed"] += 1
                    stats[outcome] += 1
                    if lane_count > 1:
                        stats[f"key_slot_{lane + 1}_processed"] += 1
                        stats[f"key_slot_{lane + 1}_{outcome}"] += 1
                    repo_name = str((item.candidate.get("repo") or {}).get("full_name") or item.key)
                    LOGGER.info(
                        "pending candidate %s finished outcome=%s key_slot=%d "
                        "processed=%d in_flight=%d",
                        repo_name,
                        outcome,
                        lane + 1,
                        stats["processed"],
                        len(futures),
                    )
                    if outcome == "key_exhausted":
                        self.queue.defer(item.key)
                        items.append(item)
                        exhausted_lanes.add(lane)
                        LOGGER.error("E2B key slot %d has exhausted its credits", lane + 1)
                    elif outcome == "error":
                        self.queue.record_attempt(item.key)
                        consecutive_errors[lane] += 1
                        if attempts.get(item.key, 0) + 1 >= max_attempts_per_item:
                            # The rejection is already recorded; remove permanently
                            # broken items so they cannot block later queue entries.
                            self.queue.complete(item.key, "error_exhausted")
                            stats["exhausted"] += 1
                        else:
                            self.queue.defer(item.key)
                    else:
                        self.queue.complete(item.key, outcome)
                        consecutive_errors[lane] = 0

                    if consecutive_errors[lane] >= max_consecutive_errors:
                        halted_lanes.add(lane)
                        if lane_count == 1:
                            stats["halted"] = 1

                refresh_items()
                for lane in range(lane_count):
                    while in_flight[lane] < max_workers and submit_next(lane):
                        pass

        if exhausted_lanes:
            stats["key_slots_exhausted"] = len(exhausted_lanes)
        if lane_count > 1 and halted_lanes:
            stats["key_slots_halted"] = len(halted_lanes)
        if len(halted_lanes | exhausted_lanes) == lane_count and items:
            stats["halted"] = 1
        stats["remaining"] = len(self.queue.pending())
        return dict(stats)

    def _verify_for_lane(
        self,
        lane: int,
        repo: dict[str, Any],
        candidate: dict[str, Any],
    ) -> str:
        if len(self.verifiers) == 1:
            return self._verify_item(repo, candidate)
        return self._verify_item_with(self.verifiers[lane], repo, candidate)

    def _verify_item(self, repo: dict[str, Any], candidate: dict[str, Any]) -> str:
        return self._verify_item_with(self.verifier, repo, candidate)

    def _verify_item_with(
        self,
        verifier: E2BCandidateVerifier | None,
        repo: dict[str, Any],
        candidate: dict[str, Any],
    ) -> str:
        if verifier is None:
            raise RuntimeError("pending verifier is not configured")
        try:
            with cloned_repository(repo["full_name"], repo["base_commit"]) as repo_path:
                return verifier.verify(
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
