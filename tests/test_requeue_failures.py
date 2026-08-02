from __future__ import annotations

import json

from alvance_github_crawler.pending.queue import (
    PendingQueue,
    build_pending_candidate,
    pending_key,
)
from alvance_github_crawler.pending.requeue import requeue_failures


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

    assert stats == {
        "matched": 1,
        "requeued": 1,
        "already_registered": 0,
        "already_requeued": 0,
    }
    assert [item.key for item in queue.pending()] == [key]


def test_requeue_skips_repositories_registered_after_the_failure(tmp_path) -> None:
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
    queue.complete(key, "registered")
    rejections = tmp_path / "rejections.jsonl"
    rejections.write_text(
        json.dumps({"repo": "owner/repository", "reason": "stage_error"}) + "\n",
        encoding="utf-8",
    )

    stats = requeue_failures(
        queue,
        rejections,
        reasons={"stage_error"},
        exclude_repos={"owner/repository"},
    )

    assert stats == {
        "matched": 0,
        "requeued": 0,
        "already_registered": 1,
        "already_requeued": 0,
    }


def test_requeue_marker_is_idempotent_across_completed_retries(tmp_path) -> None:
    queue = PendingQueue(tmp_path / "pending.jsonl")
    candidate = build_pending_candidate(
        {
            "full_name": "owner/repository",
            "language": "Go",
            "base_commit": "a" * 40,
            "source_tree": "b" * 40,
        },
        {"total": 9},
        {"direction": "Add a parser."},
    )
    key = pending_key(candidate)
    queue.enqueue(candidate)
    queue.complete(key, "error_exhausted")
    rejections = tmp_path / "rejections.jsonl"
    rejections.write_text(
        json.dumps(
            {
                "repo": "owner/repository",
                "reason": "infra_error",
                "error": "toolchain not available",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    first = requeue_failures(
        queue,
        rejections,
        reasons={"infra_error"},
        marker="go-runtime-v4",
    )
    queue.complete(key, "error_exhausted")
    second = requeue_failures(
        queue,
        rejections,
        reasons={"infra_error"},
        marker="go-runtime-v4",
    )

    assert first["requeued"] == 1
    assert second["requeued"] == 0
    assert second["already_requeued"] == 1
    assert queue.pending() == []
