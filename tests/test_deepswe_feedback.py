from __future__ import annotations

from alvance_github_crawler.deepswe_feedback import append_feedback, latest_feedback, read_feedback


def test_deepswe_feedback_records_latest_outcome(tmp_path) -> None:
    path = tmp_path / "catalog" / "deepswe-feedback.jsonl"

    append_feedback(
        path,
        repo="owner/project",
        base_commit="abcdef",
        task_id="draft/owner-project",
        outcome="abandoned",
        reason="too_shallow",
        notes="single-file change",
    )
    append_feedback(
        path,
        repo="owner/project",
        base_commit="abcdef",
        task_id="task/owner-project",
        outcome="accepted",
        reason="quality_passed",
    )

    records = read_feedback(path)
    latest = latest_feedback(path)

    assert len(records) == 2
    assert latest[("owner/project", "abcdef")]["outcome"] == "accepted"
    assert latest[("owner/project", "abcdef")]["reason"] == "quality_passed"
