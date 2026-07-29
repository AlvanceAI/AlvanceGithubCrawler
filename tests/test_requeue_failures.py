from __future__ import annotations

import json

from alvance_github_crawler.pending_queue import (
    PendingQueue,
    build_pending_candidate,
    pending_key,
)
from alvance_github_crawler.requeue_failures import requeue_failures


def test_requeue_selects_latest_matching_failure(tmp_path) -> None:
    queue = PendingQueue(tmp_path / "pending.jsonl")
    candidate = build_pending_candidate(
        {
            "full_name": "owner/repository",
            "language": "Python",
            "base_commit": "a" * 40,
            "source_tree": "b" * 40,
        },
        {"total": 9},
        {"direction": "Add a parser."},
    )
    key = pending_key(candidate)
    queue.enqueue(candidate)
    queue.complete(key, "rejected")
    rejections = tmp_path / "rejections.jsonl"
    rejections.write_text(
        json.dumps(
            {
                "repo": "owner/repository",
                "reason": "offline_test_fail",
                "offline": {"stderr_tail": "No module named pytest"},
            }
        )
        + "\n",
        encoding="utf-8",
    )

    stats = requeue_failures(
        queue,
        rejections,
        reasons={"offline_test_fail"},
        error_contains="No module named pytest",
    )

    assert stats == {"matched": 1, "requeued": 1}
    assert [item.key for item in queue.pending()] == [key]
