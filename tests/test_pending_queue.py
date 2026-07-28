from __future__ import annotations

import json

from alvance_github_crawler.pending_queue import (
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
