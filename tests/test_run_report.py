from __future__ import annotations

import json

from alvance_github_crawler.run_report import build_summary, pending_count, render_markdown


def test_run_report_tracks_pending_and_candidate_performance(tmp_path) -> None:
    crawl_dir = tmp_path / "crawl"
    production_dir = tmp_path / "production"
    crawl_dir.mkdir()
    production_dir.mkdir()
    (crawl_dir / "summary.json").write_text(
        json.dumps(
            {
                "status": "completed",
                "fetched_total": 500,
                "accepted_total": 2,
                "accepted_by_language": {"go": 2},
            }
        ),
        encoding="utf-8",
    )
    pending_path = production_dir / "pending.jsonl"
    pending_path.write_text(
        "\n".join(
            json.dumps(event)
            for event in (
                {"event": "queued", "key": "owner/one@abc"},
                {"event": "queued", "key": "owner/two@def"},
                {"event": "completed", "key": "owner/one@abc"},
            )
        )
        + "\n",
        encoding="utf-8",
    )
    (production_dir / "candidates.jsonl").write_text(
        json.dumps(
            {
                "repo": "owner/one",
                "language": "go",
                "base_commit": "a" * 40,
                "status": "ready_for_phase1",
                "e2b_environment": {
                    "cpu_count": 2,
                    "memory_mb": 4096,
                    "offline": {"duration_s": 10.0},
                },
                "benchmark": {
                    "cold_start_median_s": 0.5,
                    "test_duration_median_s": 4.0,
                    "peak_mem_median_mb": 200.0,
                },
                "harbor_package": {"task_path": "tasks/alv-one"},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    timings = tmp_path / "stage-timings.jsonl"
    timings.write_text(
        json.dumps({"stage": "crawl", "duration_s": 20, "exit_code": 0}) + "\n",
        encoding="utf-8",
    )

    summary = build_summary(
        run_id="test-run",
        crawl_dir=crawl_dir,
        production_dir=production_dir,
        timings_path=timings,
    )
    markdown = render_markdown(summary)

    assert pending_count(pending_path) == 1
    assert summary["status"] == "incomplete"
    assert summary["production"]["candidate_by_resource"] == {"2cpu-4096mb": 1}
    assert "owner/one" in markdown
    assert "2 CPU / 4096 MB" in markdown
