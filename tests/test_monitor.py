from __future__ import annotations

import runpy
from pathlib import Path

import pytest

MONITOR = runpy.run_path(str(Path(__file__).resolve().parents[1] / "monitor.py"))
build_pipeline_environment = MONITOR["build_pipeline_environment"]
candidate_summary = MONITOR["candidate_summary"]
launch_pipeline = MONITOR["launch_pipeline"]
parse_args = MONITOR["parse_args"]
pending_stats = MONITOR["pending_stats"]
rejection_summary = MONITOR["rejection_summary"]


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


def test_default_launcher_environment_enables_full_dual_key_pipeline(tmp_path: Path) -> None:
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
