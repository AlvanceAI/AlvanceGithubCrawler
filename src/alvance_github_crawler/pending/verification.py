from __future__ import annotations

import json
import logging
import time
from collections import Counter, deque
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ..catalog.harbor_packaging import HarborPackager
from ..config import PipelineConfig
from ..e2b.verification import E2BCandidateVerifier
from ..registry import JsonlRegistry
from ..screening.scoring import LanguageQuota
from ..workspace import cloned_repository
from .queue import PendingItem, PendingQueue, _parse_datetime
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
                    template_build_timeout_s=config.e2b_template_build_timeout_s,
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
        follow_until: Path | None = None,
        poll_interval_s: float = 1.0,
        status_path: Path | None = None,
    ) -> dict[str, int]:
        if max_workers < 1:
            raise ValueError("max_workers must be >= 1")
        if max_attempts_per_item < 1:
            raise ValueError("max_attempts_per_item must be >= 1")
        if poll_interval_s <= 0:
            raise ValueError("poll_interval_s must be > 0")
        stats: Counter[str] = Counter()
        registered = self.registry.existing_repos()
        attempts = self.queue.attempt_counts()
        items: deque[Any] = deque()
        follow_active: dict[str, PendingItem] | None = None
        follow_offset = 0
        if follow_until is not None:
            # Take a stable append-only snapshot. If a prescreen worker appends
            # while the snapshot is being read, retry until the file size is
            # unchanged; later appends are then observed by events_since().
            while True:
                try:
                    snapshot_start = self.queue.path.stat().st_size
                except OSError:
                    snapshot_start = 0
                initial_pending = self.queue.pending()
                try:
                    snapshot_end = self.queue.path.stat().st_size
                except OSError:
                    snapshot_end = snapshot_start
                if snapshot_start == snapshot_end:
                    follow_offset = snapshot_end
                    break
            follow_active = {item.key: item for item in initial_pending}
            now = datetime.now(UTC)
            initial_items = [
                item
                for item in initial_pending
                if item.retry_at is None or item.retry_at <= now
            ]
        else:
            initial_items = self.queue.ready()
        for item in initial_items:
            candidate = item.candidate
            repo = dict(candidate["repo"])
            if str(repo.get("full_name") or "") in registered:
                # Crash between register and complete leaves the item active;
                # never re-verify or re-register an already-registered repo.
                self.queue.complete(item.key, "already_registered")
                stats["already_registered"] += 1
                if follow_active is not None:
                    follow_active.pop(item.key, None)
                continue
            if max_items is not None and len(items) >= max_items:
                break
            items.append(item)
        scheduled_keys = {item.key for item in items}

        lane_count = len(self.verifiers)
        total_workers = max_workers * lane_count
        consecutive_errors = [0] * lane_count
        in_flight = [0] * lane_count
        lane_limits = [max_workers] * lane_count
        lane_successes = [0] * lane_count
        halted_lanes: set[int] = set()
        exhausted_lanes: set[int] = set()
        next_lane = 0
        started_at = time.time()

        def write_status(state: str) -> None:
            if status_path is None:
                return
            payload = {
                "state": state,
                "updated_at": time.time(),
                "started_at": started_at,
                "follow": follow_until is not None,
                "processed": int(stats.get("processed", 0)),
                "processed_rate_per_hour": int(stats.get("processed", 0))
                * 3600.0
                / max(1.0, time.time() - started_at),
                "pending": (
                    len(follow_active)
                    if follow_active is not None
                    else len(self.queue.pending())
                ),
                "in_flight": len(futures),
                "in_flight_by_key": {
                    f"key_slot_{lane + 1}": in_flight[lane] for lane in range(lane_count)
                },
                "capacity_by_key": {
                    f"key_slot_{lane + 1}": lane_limits[lane] for lane in range(lane_count)
                },
                "max_workers_per_key": max_workers,
                "key_slots": lane_count,
            }
            status_path.parent.mkdir(parents=True, exist_ok=True)
            temporary = status_path.with_suffix(status_path.suffix + ".tmp")
            temporary.write_text(
                json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            temporary.replace(status_path)

        with ThreadPoolExecutor(
            max_workers=total_workers,
            thread_name_prefix="e2b-verify",
        ) as pool:
            futures: dict[Future[str], tuple[Any, int]] = {}

            def refresh_items() -> None:
                if max_items is not None:
                    return
                nonlocal follow_offset
                if follow_active is not None:
                    events, follow_offset = self.queue.events_since(follow_offset)
                    for event in events:
                        key = str(event.get("key") or "")
                        if not key:
                            continue
                        event_name = str(event.get("event") or "")
                        candidate = event.get("candidate")
                        if event_name in {"queued", "requeued"} and isinstance(
                            candidate, dict
                        ):
                            follow_active[key] = PendingItem(
                                key=key,
                                candidate=dict(candidate),
                            )
                        elif event_name == "deferred":
                            pending_item = follow_active.get(key)
                            if pending_item is not None:
                                follow_active[key] = replace(
                                    pending_item,
                                    retry_at=_parse_datetime(event.get("retry_at")),
                                )
                            scheduled_keys.discard(key)
                        elif event_name == "completed":
                            follow_active.pop(key, None)
                            scheduled_keys.discard(key)
                    now = datetime.now(UTC)
                    pending_items = list(follow_active.values())
                else:
                    pending_items = self.queue.ready()
                for pending_item in pending_items:
                    if follow_active is not None:
                        if pending_item.retry_at is not None and pending_item.retry_at > now:
                            continue
                    if follow_active is not None:
                        repo = dict(pending_item.candidate.get("repo") or {})
                        if str(repo.get("full_name") or "") in registered:
                            self.queue.complete(pending_item.key, "already_registered")
                            follow_active.pop(pending_item.key, None)
                            scheduled_keys.discard(pending_item.key)
                            stats["already_registered"] += 1
                            continue
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

            def fill_available_slots() -> None:
                nonlocal next_lane
                while items:
                    available = [
                        lane
                        for lane in range(lane_count)
                        if in_flight[lane] < lane_limits[lane]
                        and lane not in halted_lanes
                        and lane not in exhausted_lanes
                    ]
                    if not available:
                        return
                    minimum_in_flight = min(in_flight[lane] for lane in available)
                    least_loaded = {
                        lane
                        for lane in available
                        if in_flight[lane] == minimum_in_flight
                    }
                    lane = next(
                        lane
                        for offset in range(lane_count)
                        if (lane := (next_lane + offset) % lane_count) in least_loaded
                    )
                    if not submit_next(lane):
                        return
                    next_lane = (lane + 1) % lane_count

            fill_available_slots()
            write_status("running" if futures else "waiting_for_pending")

            while True:
                if not futures:
                    refresh_items()
                    fill_available_slots()
                    if futures:
                        write_status("running")
                        continue

                    all_lanes_blocked = len(halted_lanes | exhausted_lanes) == lane_count
                    pending_total = (
                        len(follow_active)
                        if follow_active is not None
                        else len(self.queue.pending())
                    )
                    if all_lanes_blocked and (items or pending_total):
                        if follow_until is not None and halted_lanes and not exhausted_lanes:
                            # Temporary infrastructure errors should cool down and
                            # retry while the upstream producer is still alive.
                            halted_lanes.clear()
                            consecutive_errors = [0] * lane_count
                            write_status("cooling_down")
                            time.sleep(poll_interval_s)
                            continue
                        break
                    if follow_until is not None and not follow_until.is_file():
                        write_status("waiting_for_pending")
                        time.sleep(poll_interval_s)
                        continue
                    if follow_until is not None and pending_total:
                        # Deferred rate-limit/error items can become ready later.
                        write_status("waiting_for_retry")
                        time.sleep(poll_interval_s)
                        continue
                    break

                completed, _ = wait(
                    futures,
                    timeout=1,
                    return_when=FIRST_COMPLETED,
                )
                for future in completed:
                    item, lane = futures.pop(future)
                    in_flight[lane] -= 1
                    try:
                        outcome = future.result()
                    except Exception:
                        LOGGER.exception("pending verification worker failed")
                        outcome = "error"
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
                        if follow_until is None:
                            items.append(item)
                        else:
                            scheduled_keys.discard(item.key)
                        exhausted_lanes.add(lane)
                        LOGGER.error("E2B key slot %d has exhausted its credits", lane + 1)
                    elif outcome == "rate_limited":
                        self.queue.defer(item.key, delay_s=60)
                        if follow_until is not None:
                            scheduled_keys.discard(item.key)
                        consecutive_errors[lane] = 0
                        lane_successes[lane] = 0
                        previous_limit = lane_limits[lane]
                        lane_limits[lane] = max(1, previous_limit - 1)
                        if lane_limits[lane] < previous_limit:
                            stats[f"key_slot_{lane + 1}_capacity_reductions"] += 1
                        LOGGER.warning(
                            "E2B key slot %d rate limited; capacity=%d retry_delay_s=60",
                            lane + 1,
                            lane_limits[lane],
                        )
                    elif outcome == "error":
                        self.queue.record_attempt(item.key)
                        attempt_number = attempts.get(item.key, 0) + 1
                        attempts[item.key] = attempt_number
                        consecutive_errors[lane] += 1
                        lane_successes[lane] = 0
                        if attempt_number >= max_attempts_per_item:
                            # The rejection is already recorded; remove permanently
                            # broken items so they cannot block later queue entries.
                            self.queue.complete(item.key, "error_exhausted")
                            stats["exhausted"] += 1
                        else:
                            delays = (15, 60, 180)
                            delay_s = delays[min(attempt_number - 1, len(delays) - 1)]
                            self.queue.defer(item.key, delay_s=delay_s)
                            if follow_until is not None:
                                scheduled_keys.discard(item.key)
                    else:
                        self.queue.complete(item.key, outcome)
                        if outcome == "registered":
                            registered.add(repo_name)
                        consecutive_errors[lane] = 0
                        halted_lanes.discard(lane)
                        lane_successes[lane] += 1
                        if (
                            lane_limits[lane] < max_workers
                            and lane_successes[lane] >= lane_limits[lane]
                        ):
                            lane_limits[lane] += 1
                            lane_successes[lane] = 0
                            stats[f"key_slot_{lane + 1}_capacity_recoveries"] += 1

                    if consecutive_errors[lane] >= max_consecutive_errors:
                        halted_lanes.add(lane)
                        if lane_count == 1:
                            stats["halted"] = 1

                refresh_items()
                fill_available_slots()
                write_status("running" if futures else "waiting_for_pending")

        if exhausted_lanes:
            stats["key_slots_exhausted"] = len(exhausted_lanes)
        if lane_count > 1 and halted_lanes:
            stats["key_slots_halted"] = len(halted_lanes)
        if len(halted_lanes | exhausted_lanes) == lane_count and items:
            stats["halted"] = 1
        stats["remaining"] = (
            len(follow_active) if follow_active is not None else len(self.queue.pending())
        )
        if status_path is not None:
            payload = {
                "state": "complete" if not stats.get("halted") else "halted",
                "updated_at": time.time(),
                "started_at": started_at,
                "follow": follow_until is not None,
                "processed": int(stats.get("processed", 0)),
                "processed_rate_per_hour": int(stats.get("processed", 0))
                * 3600.0
                / max(1.0, time.time() - started_at),
                "pending": int(stats["remaining"]),
                "in_flight": 0,
                "in_flight_by_key": {
                    f"key_slot_{lane + 1}": in_flight[lane] for lane in range(lane_count)
                },
                "capacity_by_key": {
                    f"key_slot_{lane + 1}": lane_limits[lane] for lane in range(lane_count)
                },
                "max_workers_per_key": max_workers,
                "key_slots": lane_count,
            }
            status_path.parent.mkdir(parents=True, exist_ok=True)
            temporary = status_path.with_suffix(status_path.suffix + ".tmp")
            temporary.write_text(
                json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            temporary.replace(status_path)
        return dict(stats)

    def run_follow(
        self,
        *,
        until_path: Path,
        max_workers: int = 1,
        poll_interval_s: float = 1.0,
        status_path: Path | None = None,
    ) -> dict[str, int]:
        """Keep the E2B lanes alive until the upstream follower has finished."""
        return self.run(
            max_workers=max_workers,
            follow_until=until_path,
            poll_interval_s=poll_interval_s,
            status_path=status_path,
        )

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
