from __future__ import annotations

import json
import threading
import time
from pathlib import Path

from alvance_github_crawler.jsonl_io import IncrementalJSONLReader
from alvance_github_crawler.pending.queue import PendingQueue
from alvance_github_crawler.pending.verification import PendingVerificationRunner
from alvance_github_crawler.pipeline import Pipeline


def make_candidate(index: int) -> dict[str, object]:
    return {
        "repo": {
            "full_name": f"owner/repository-{index}",
            "base_commit": str(index) * 40,
            "language": "python",
        }
    }


def test_incremental_reader_waits_for_complete_line_and_resumes(tmp_path: Path) -> None:
    source = tmp_path / "accepted.jsonl"
    cursor_path = tmp_path / "accepted.cursor.json"
    source.write_text(json.dumps(make_candidate(0)), encoding="utf-8")
    reader = IncrementalJSONLReader(source, cursor_path)

    partial = reader.read()
    assert partial.records == []
    assert partial.next_offset == 0

    with source.open("a", encoding="utf-8") as handle:
        handle.write("\n")
    batch = reader.read()
    assert len(batch.records) == 1
    reader.commit(batch)
    assert json.loads(cursor_path.read_text(encoding="utf-8"))["offset"] == source.stat().st_size

    with source.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(make_candidate(1)) + "\n")
    next_batch = reader.read()
    assert [row["repo"]["full_name"] for row in next_batch.records] == [
        "owner/repository-1"
    ]


def test_pending_follow_waits_when_queue_is_initially_empty(tmp_path: Path, monkeypatch) -> None:
    queue = PendingQueue(tmp_path / "pending.jsonl")

    class Registry:
        @staticmethod
        def existing_repos() -> set[str]:
            return set()

    runner = PendingVerificationRunner(queue, registry=Registry(), verifier=None)  # type: ignore[arg-type]
    done = tmp_path / "prescreen.done"
    result: dict[str, dict[str, int]] = {}
    monkeypatch.setattr(runner, "_verify_item", lambda repo, candidate: "registered")

    thread = threading.Thread(
        target=lambda: result.setdefault(
            "stats",
            runner.run_follow(until_path=done, max_workers=2, poll_interval_s=0.01),
        )
    )
    thread.start()
    time.sleep(0.05)
    assert thread.is_alive()
    queue.enqueue(make_candidate(0))
    done.touch()
    thread.join(timeout=2)

    assert not thread.is_alive()
    assert result["stats"]["registered"] == 1
    assert result["stats"]["remaining"] == 0


def test_pending_follow_reroutes_exhausted_lane_without_duplicate_submission(
    tmp_path: Path,
) -> None:
    queue = PendingQueue(tmp_path / "pending.jsonl")
    queue.enqueue(make_candidate(0))
    done = tmp_path / "prescreen.done"
    done.touch()
    exhausted = object()
    available = object()
    runner = PendingVerificationRunner(
        queue,
        registry=type("Registry", (), {"existing_repos": staticmethod(lambda: set())})(),
        verifier=exhausted,  # type: ignore[arg-type]
        verifiers=(exhausted, available),  # type: ignore[arg-type]
    )

    def verify(verifier, repo, candidate):
        return "key_exhausted" if verifier is exhausted else "registered"

    runner._verify_item_with = verify  # type: ignore[method-assign]
    stats = runner.run_follow(until_path=done, max_workers=1, poll_interval_s=0.01)

    assert stats["key_slots_exhausted"] == 1
    assert stats["registered"] == 1
    assert stats["remaining"] == 0


def test_pipeline_follow_consumes_records_appended_after_start(tmp_path: Path) -> None:
    accepted = tmp_path / "accepted.jsonl"
    cursor = tmp_path / "accepted.cursor.json"
    done = tmp_path / "crawl.done"
    accepted.write_text("", encoding="utf-8")

    class Registry:
        @staticmethod
        def existing_repos() -> set[str]:
            return set()

        @staticmethod
        def terminal_rejections() -> set[str]:
            return set()

    class Pending:
        @staticmethod
        def known_repos() -> set[str]:
            return set()

        @staticmethod
        def pending() -> list[object]:
            return []

        @staticmethod
        def active_count() -> int:
            return 0

    pipeline = object.__new__(Pipeline)
    pipeline.registry = Registry()
    pipeline.pending = Pending()
    pipeline.retry_rejected = False
    pipeline.config = type("Config", (), {"catalog_dir": tmp_path, "prescreen_concurrency": 2})()
    pipeline._process_crawl_candidate = lambda candidate: "queued"  # type: ignore[method-assign]
    result: dict[str, dict[str, int]] = {}

    thread = threading.Thread(
        target=lambda: result.setdefault(
            "stats",
            pipeline.run_crawl_candidates_follow(
                accepted,
                cursor_path=cursor,
                producer_done_path=done,
                poll_interval_s=0.01,
            ),
        )
    )
    thread.start()
    time.sleep(0.05)
    assert thread.is_alive()
    with accepted.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(make_candidate(0)) + "\n")
    done.touch()
    thread.join(timeout=2)

    assert not thread.is_alive()
    assert result["stats"]["queued"] == 1
    assert json.loads(cursor.read_text(encoding="utf-8"))["offset"] == accepted.stat().st_size
