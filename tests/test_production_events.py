from __future__ import annotations

from alvance_github_crawler.production_events import ProductionEventWriter, read_events
from alvance_github_crawler.registry import JsonlRegistry


def test_production_events_can_be_read_after_registry_actions(tmp_path) -> None:
    events_path = tmp_path / "events.jsonl"
    registry = JsonlRegistry(
        tmp_path / "candidates.jsonl",
        tmp_path / "rejections.jsonl",
        events_path=events_path,
    )

    registry.register({"repo": "owner/project"})
    registry.reject({"full_name": "bad/project"}, "score", "low_score")

    events = read_events(events_path)

    assert [event["event_type"] for event in events] == [
        "candidate_registered",
        "candidate_rejected",
    ]
    assert events[0]["repo"] == "owner/project"
    assert events[1]["reason"] == "low_score"


def test_event_writer_is_noop_without_path() -> None:
    ProductionEventWriter(None).emit(
        stage="stage",
        event_type="event",
        status="ok",
        repo="owner/project",
    )
