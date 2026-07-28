from __future__ import annotations

import json

from alvance_github_crawler.harbor_packaging import (
    compact_package_record,
    harbor_task_name,
    harbor_template_alias,
    write_task_envelope,
)


def test_harbor_envelope_is_tiny_and_deterministic(tmp_path) -> None:
    repo = "owner/example-repository"
    commit = "a" * 40
    task_name = harbor_task_name(repo, commit)
    task_dir = tmp_path / "catalog" / "harbor" / task_name
    envs = {"PATH": "/usr/local/bin:/usr/bin", "HOME": "/root"}

    write_task_envelope(
        task_dir,
        task_name=task_name,
        repo=repo,
        base_commit=commit,
        language="python",
        direction="Add the requested feature.",
        source_template_alias="source-template-v1",
        test_cmd="python -m pytest -q",
        envs=envs,
    )

    first = harbor_template_alias(task_dir)
    second = harbor_template_alias(task_dir)
    assert first == second
    assert first.startswith(f"{task_name}__")
    assert sum(path.stat().st_size for path in task_dir.rglob("*") if path.is_file()) < 10_000
    assert "source-template-v1" in (task_dir / "environment" / "Dockerfile").read_text()
    assert "python -m pytest -q" in (task_dir / "tests" / "test.sh").read_text()


def test_compact_package_omits_test_logs() -> None:
    class Result:
        package_id = "pkg"
        task_name = "task"
        task_path = "catalog/harbor/task"
        source_template_alias = "source"
        source_template_id = "source-id"
        harbor_template_alias = "harbor"
        harbor_template_id = "harbor-id"
        smoke_ok = True
        launch_command = "harbor run"

    record = {
        "repo": "owner/repo",
        "base_commit": "a" * 40,
        "language": "go",
        "test_cmd": "go test ./...",
        "e2b_environment": {
            "runtime_version": "1.22",
            "offline": {"ok": True, "duration_s": 1.0, "stdout_tail": "large log"},
        },
        "benchmark": {
            "cold_start_median_s": 0.5,
            "test_duration_median_s": 2.0,
            "peak_mem_median_mb": 100.0,
            "stable": True,
        },
    }
    payload = compact_package_record(record, Result(), {"PATH": "/usr/bin"})
    serialized = json.dumps(payload)
    assert "large log" not in serialized
    assert payload["storage"]["remote_e2b_only"] is True
