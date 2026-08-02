from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

from alvance_github_crawler.pending.queue import (
    PendingQueue,
    build_pending_candidate,
    pending_key,
)


def candidate() -> dict[str, object]:
    return build_pending_candidate(
        {
            "full_name": "owner/repository",
            "name": "repository",
            "language": "Go",
            "base_commit": "a" * 40,
            "source_tree": "b" * 40,
            "private_field": "discarded",
        },
        {"total": 9, "file_count": 200},
        {"source": "issue#1", "direction": "Add a parser.", "target_paths": []},
    )


def test_pending_queue_is_idempotent_and_recoverable(tmp_path) -> None:
    queue = PendingQueue(tmp_path / "pending.jsonl")
    item = candidate()
    key = pending_key(item)

    assert queue.enqueue(item) is True
    assert queue.enqueue(item) is False
    queue.record_attempt(key)
    assert [pending.key for pending in queue.pending()] == [key]

    queue.complete(key, "registered")
    assert queue.pending() == []
    assert queue.known_repos() == {"owner/repository"}
    assert queue.requeue(key) is True
    assert [pending.key for pending in queue.pending()] == [key]
    assert queue.requeue(key) is False


def test_pending_record_contains_only_control_plane_fields(tmp_path) -> None:
    path = tmp_path / "pending.jsonl"
    queue = PendingQueue(path)
    queue.enqueue(candidate())

    payload = json.loads(path.read_text().splitlines()[0])

    assert "private_field" not in payload["candidate"]["repo"]
    assert len(path.read_bytes()) < 5_000


def test_pending_queue_distinguishes_commits(tmp_path) -> None:
    queue = PendingQueue(tmp_path / "pending.jsonl")
    first = candidate()
    second = candidate()
    second["repo"]["base_commit"] = "c" * 40

    assert queue.enqueue(first) is True
    assert queue.enqueue(second) is True
    assert len(queue.pending()) == 2


def test_defer_moves_item_to_tail(tmp_path) -> None:
    queue = PendingQueue(tmp_path / "pending.jsonl")
    first = candidate()
    second = candidate()
    second["repo"]["base_commit"] = "c" * 40
    queue.enqueue(first)
    queue.enqueue(second)

    queue.defer(pending_key(first))

    assert [item.key for item in queue.pending()] == [
        pending_key(second),
        pending_key(first),
    ]


def test_deferred_item_is_not_ready_until_retry_time(tmp_path) -> None:
    queue = PendingQueue(tmp_path / "pending.jsonl")
    item = candidate()
    key = pending_key(item)
    queue.enqueue(item)
    queue.defer(key, delay_s=60)

    now = datetime.now(UTC)
    assert queue.ready(now=now) == []
    assert [pending.key for pending in queue.ready(now=now + timedelta(seconds=61))] == [
        key
    ]


def test_completed_item_can_be_enqueued_again(tmp_path) -> None:
    queue = PendingQueue(tmp_path / "pending.jsonl")
    item = candidate()
    key = pending_key(item)
    queue.enqueue(item)
    queue.complete(key, "rejected")

    assert queue.enqueue(item) is True
    assert [pending.key for pending in queue.pending()] == [key]


def test_attempt_counts_and_active_repos(tmp_path) -> None:
    queue = PendingQueue(tmp_path / "pending.jsonl")
    item = candidate()
    key = pending_key(item)
    queue.enqueue(item)
    queue.record_attempt(key)
    queue.record_attempt(key)

    assert queue.attempt_counts() == {key: 2}
    assert queue.active_repos() == {"owner/repository"}

    queue.complete(key, "error_exhausted")
    assert queue.active_repos() == set()
    assert queue.known_repos() == {"owner/repository"}


def test_requeue_starts_a_fresh_attempt_cycle(tmp_path) -> None:
    queue = PendingQueue(tmp_path / "pending.jsonl")
    item = candidate()
    key = pending_key(item)
    queue.enqueue(item)
    queue.record_attempt(key)
    queue.record_attempt(key)
    queue.complete(key, "error_exhausted")

    assert queue.requeue(key, marker="recipe-v2") is True
    assert queue.attempt_counts() == {}

    queue.record_attempt(key)
    assert queue.attempt_counts() == {key: 1}


def test_active_count_tracks_appended_tail(tmp_path) -> None:
    queue = PendingQueue(tmp_path / "pending.jsonl")
    first = candidate()
    second = candidate()
    second["repo"]["base_commit"] = "c" * 40

    assert queue.active_count() == 0
    assert queue.enqueue(first)
    assert queue.active_count() == 1
    queue.complete(pending_key(first), "registered")
    assert queue.active_count() == 0
    assert queue.enqueue(second)
    assert queue.active_count() == 1
