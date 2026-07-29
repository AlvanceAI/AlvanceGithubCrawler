from __future__ import annotations

from alvance_github_crawler.pending.queue import (
    PendingQueue,
    build_pending_candidate,
    pending_key,
)
from alvance_github_crawler.pending.verification import PendingVerificationRunner


class StubRegistry:
    def __init__(self, registered: set[str] | None = None) -> None:
        self.registered = registered or set()

    def existing_repos(self) -> set[str]:
        return set(self.registered)


def make_candidate(index: int) -> dict[str, object]:
    return build_pending_candidate(
        {
            "full_name": f"owner/repository-{index}",
            "language": "Python",
            "base_commit": str(index) * 40,
            "source_tree": "a" * 40,
        },
        {"total": 9},
        {"direction": "Add a parser."},
    )


def filled_queue(tmp_path, count: int = 5) -> PendingQueue:
    queue = PendingQueue(tmp_path / "pending.jsonl")
    for index in range(count):
        queue.enqueue(make_candidate(index))
    return queue


def test_runner_stops_after_consecutive_infrastructure_errors(tmp_path, monkeypatch) -> None:
    queue = filled_queue(tmp_path)
    runner = PendingVerificationRunner(queue, registry=StubRegistry(), verifier=None)  # type: ignore[arg-type]
    monkeypatch.setattr(runner, "_verify_item", lambda repo, candidate: "error")

    stats = runner.run(max_consecutive_errors=3)

    assert stats == {"processed": 3, "error": 3, "halted": 1, "remaining": 5}


def test_runner_defers_failed_items_to_queue_tail(tmp_path, monkeypatch) -> None:
    queue = filled_queue(tmp_path, count=3)
    runner = PendingVerificationRunner(queue, registry=StubRegistry(), verifier=None)  # type: ignore[arg-type]
    outcomes = iter(["error", "registered", "registered"])
    monkeypatch.setattr(runner, "_verify_item", lambda repo, candidate: next(outcomes))

    stats = runner.run(max_consecutive_errors=3)

    assert stats["processed"] == 3
    assert stats["registered"] == 2
    assert stats["remaining"] == 1
    # The failed head item stays active but no longer blocks the queue.
    remaining = queue.pending()
    assert [item.key for item in remaining] == [pending_key(make_candidate(0))]


def test_runner_evicts_items_after_attempt_limit(tmp_path, monkeypatch) -> None:
    queue = filled_queue(tmp_path, count=1)
    runner = PendingVerificationRunner(queue, registry=StubRegistry(), verifier=None)  # type: ignore[arg-type]
    monkeypatch.setattr(runner, "_verify_item", lambda repo, candidate: "error")

    for expected_remaining in (1, 1, 0):
        stats = runner.run(max_consecutive_errors=10)
        assert stats["remaining"] == expected_remaining

    assert queue.pending() == []


def test_runner_skips_already_registered_repos(tmp_path, monkeypatch) -> None:
    queue = filled_queue(tmp_path, count=2)
    registry = StubRegistry({"owner/repository-0"})
    runner = PendingVerificationRunner(queue, registry=registry, verifier=None)  # type: ignore[arg-type]
    verified: list[str] = []

    def record(repo, candidate):
        verified.append(repo["full_name"])
        return "registered"

    monkeypatch.setattr(runner, "_verify_item", record)

    stats = runner.run()

    assert verified == ["owner/repository-1"]
    assert stats["already_registered"] == 1
    assert stats["processed"] == 1
    assert queue.pending() == []
