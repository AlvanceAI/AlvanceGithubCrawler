from __future__ import annotations

from alvance_github_crawler.pending_queue import PendingQueue, build_pending_candidate
from alvance_github_crawler.pending_verification import PendingVerificationRunner


def test_runner_stops_after_consecutive_infrastructure_errors(tmp_path, monkeypatch) -> None:
    queue = PendingQueue(tmp_path / "pending.jsonl")
    for index in range(5):
        queue.enqueue(
            build_pending_candidate(
                {
                    "full_name": f"owner/repository-{index}",
                    "language": "Python",
                    "base_commit": str(index) * 40,
                    "source_tree": "a" * 40,
                },
                {"total": 9},
                {"direction": "Add a parser."},
            )
        )
    runner = PendingVerificationRunner(queue, registry=None, verifier=None)  # type: ignore[arg-type]
    monkeypatch.setattr(runner, "_verify_item", lambda repo, candidate: "error")

    stats = runner.run(max_consecutive_errors=3)

    assert stats == {"processed": 3, "error": 3, "halted": 1, "remaining": 5}
