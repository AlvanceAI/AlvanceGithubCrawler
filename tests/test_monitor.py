from __future__ import annotations

import runpy
from datetime import UTC, datetime
from pathlib import Path

import pytest

MONITOR = runpy.run_path(str(Path(__file__).resolve().parents[1] / "monitor.py"))
build_pipeline_environment = MONITOR["build_pipeline_environment"]
candidate_summary = MONITOR["candidate_summary"]
checkpoint_per_language = MONITOR["checkpoint_per_language"]
launch_pipeline = MONITOR["launch_pipeline"]
parse_args = MONITOR["parse_args"]
pending_stats = MONITOR["pending_stats"]
pipeline_exit_action = MONITOR["pipeline_exit_action"]
rejection_summary = MONITOR["rejection_summary"]
task_rate_summary = MONITOR["task_rate_summary"]


def test_pending_stats_replays_append_only_queue() -> None:
    records = [
        {"event": "queued", "key": "a", "candidate": {"repo": "owner/a"}},
        {"event": "queued", "key": "b", "candidate": {"repo": "owner/b"}},
        {"event": "attempted", "key": "a"},
        {"event": "completed", "key": "a"},
        {"event": "requeued", "key": "c", "candidate": {"repo": "owner/c"}},
    ]

    assert pending_stats(records) == {"active": 2, "attempts": {"a": 1}}


def test_rejection_summary_uses_latest_reason_per_repository() -> None:
    records = [
        {"repo": "owner/a", "reason": "build_fail"},
        {"repo": "owner/b", "reason": "no_direction"},
        {"repo": "owner/a", "reason": "offline_test_fail"},
    ]

    assert rejection_summary(records) == {
        "offline_test_fail": 1,
        "no_direction": 1,
    }


def test_candidate_summary_deduplicates_task_path_not_repository() -> None:
    records = [
        {
            "repo": "owner/repo",
            "base_commit": "one",
            "language": "python",
            "harbor_package": {"task_path": "tasks/one"},
        },
        {
            "repo": "owner/repo",
            "base_commit": "two",
            "language": "python",
            "harbor_package": {"task_path": "tasks/two"},
        },
        {
            "repo": "owner/repo",
            "base_commit": "one",
            "language": "python",
            "harbor_package": {"task_path": "tasks/one"},
        },
    ]

    assert candidate_summary(records) == {"python": 2}


def test_task_rate_summary_uses_unique_registered_tasks_in_rolling_windows() -> None:
    now = datetime(2026, 7, 30, 12, 0, tzinfo=UTC)
    records = [
        {
            "repo": "owner/a",
            "base_commit": "one",
            "harbor_package": {"task_path": "tasks/a"},
            "registered_at": "2026-07-30T11:55:00+00:00",
        },
        {
            "repo": "owner/a",
            "base_commit": "one",
            "harbor_package": {"task_path": "tasks/a"},
            "registered_at": "2026-07-30T11:59:00+00:00",
        },
        {
            "repo": "owner/b",
            "base_commit": "two",
            "registered_at": "2026-07-30T11:46:00Z",
        },
        {
            "repo": "owner/c",
            "base_commit": "three",
            "registered_at": "2026-07-30T11:30:00+00:00",
        },
        {
            "repo": "owner/d",
            "base_commit": "four",
            "registered_at": "2026-07-30T10:50:00+00:00",
        },
        {"repo": "owner/bad", "registered_at": "not-a-timestamp"},
    ]

    summary = task_rate_summary(records, now=now)

    assert summary["last_15m_count"] == 2
    assert summary["last_15m_per_hour"] == 8.0
    assert summary["last_60m_count"] == 3
    assert summary["last_60m_per_hour"] == 3.0
    assert summary["latest_at"] == datetime(2026, 7, 30, 11, 55, tzinfo=UTC)


def launcher_args(tmp_path: Path):
    return parse_args(
        [
            str(tmp_path / "production"),
            "--crawl-dir",
            str(tmp_path / "crawl"),
            "--run-root",
            str(tmp_path / "runs"),
            "--run-id",
            "test-production-run",
        ]
    )


def test_default_launcher_environment_enables_full_dual_key_pipeline(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PIPELINE_WORKSPACE_TMPDIR", str(tmp_path / "workspace"))
    monkeypatch.setenv("PIPELINE_WORKSPACE_MIN_FREE_MB", "20480")
    monkeypatch.setenv("PIPELINE_WORKSPACE_MAX_MB", "51200")
    monkeypatch.setenv("PIPELINE_WORKSPACE_RESERVATION_MB", "640")
    monkeypatch.setenv("PIPELINE_WORKSPACE_QUOTA_WAIT_S", "900")
    args = launcher_args(tmp_path)

    environment = build_pipeline_environment(args, ceiling_per_language=2_000)

    assert environment["PIPELINE_RUN_ID"] == "test-production-run"
    assert environment["CRAWL_OUTPUT_DIR"] == str(tmp_path / "crawl")
    assert environment["PRODUCTION_OUTPUT_DIR"] == str(tmp_path / "production")
    assert environment["PUBLISH_BRANCH"] == "XBY"
    assert environment["MAX_PER_LANGUAGE"] == "2000"
    assert environment["BATCH_PER_LANGUAGE"] == "100"
    assert environment["PRESCREEN_CONCURRENCY"] == "20"
    assert environment["E2B_CONCURRENCY"] == "20"
    assert environment["PUBLISH_TASKS"] == "true"
    assert environment["PUBLISH_RUN_ARTIFACTS"] == "true"
    assert environment["AUTO_GIT_PUSH"] == "false"
    assert environment["PIPELINE_WORKSPACE_TMPDIR"] == str(tmp_path / "workspace")
    assert environment["PIPELINE_WORKSPACE_MIN_FREE_MB"] == "20480"
    assert environment["PIPELINE_WORKSPACE_MAX_MB"] == "51200"
    assert environment["PIPELINE_WORKSPACE_RESERVATION_MB"] == "640"
    assert environment["PIPELINE_WORKSPACE_QUOTA_WAIT_S"] == "900"


def test_checkpoint_ceiling_never_drops_below_existing_target(tmp_path: Path) -> None:
    crawl_dir = tmp_path / "crawl"
    crawl_dir.mkdir()
    (crawl_dir / "crawl_state.json").write_text(
        '{"target_total":38500,"per_language":7700}',
        encoding="utf-8",
    )

    assert checkpoint_per_language(crawl_dir) == 7_700


@pytest.mark.parametrize(
    (
        "return_code",
        "stop_at_max",
        "exhausted",
        "cycle_completed",
        "source_exhausted",
        "expected",
    ),
    [
        (0, False, False, True, False, "extend"),
        (0, True, False, True, False, "complete"),
        (0, False, False, False, False, "failed"),
        (1, False, False, True, False, "failed"),
        (4, False, True, False, False, "exhausted"),
        (0, False, False, True, True, "source_exhausted"),
    ],
)
def test_pipeline_exit_action_requires_a_successful_cycle_marker(
    return_code: int,
    stop_at_max: bool,
    exhausted: bool,
    cycle_completed: bool,
    source_exhausted: bool,
    expected: str,
) -> None:
    assert (
        pipeline_exit_action(
            return_code,
            stop_at_max=stop_at_max,
            exhausted=exhausted,
            cycle_completed=cycle_completed,
            source_exhausted=source_exhausted,
        )
        == expected
    )


def test_launch_pipeline_runs_continuous_driver_in_new_process_group(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    args = launcher_args(tmp_path)
    observed: dict[str, object] = {}

    class StubProcess:
        pid = 12345

    def fake_popen(command, **kwargs):
        observed["command"] = command
        observed.update(kwargs)
        return StubProcess()

    monkeypatch.setattr(MONITOR["subprocess"], "Popen", fake_popen)

    managed = launch_pipeline(args, ceiling_per_language=2_000)
    managed.close_log()

    assert observed["command"] == [
        "bash",
        str(MONITOR["REPO_ROOT"] / "scripts/run_continuous_production.sh"),
    ]
    assert observed["cwd"] == MONITOR["REPO_ROOT"]
    assert observed["start_new_session"] is True
    assert observed["stderr"] is MONITOR["subprocess"].STDOUT
    assert managed.log_path == tmp_path / "runs/test-production-run/logs/launcher.log"


def test_parse_args_rejects_unsafe_run_id(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        parse_args(
            [
                str(tmp_path / "production"),
                "--run-id",
                "../outside-run-root",
            ]
        )
