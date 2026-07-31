from __future__ import annotations

import json

from alvance_github_crawler.material_export import (
    has_ready_e2b_material,
    load_candidate_records,
    prepare_materials,
    select_records,
)


def test_load_select_and_prepare_ready_materials(tmp_path) -> None:
    crawler_dir = tmp_path / "crawler"
    state_dir = crawler_dir / ".crawler-state"
    state_dir.mkdir(parents=True)
    (crawler_dir / "materials" / "owner-repo" / "environment").mkdir(parents=True)
    (crawler_dir / "materials" / "owner-repo" / "environment" / "Dockerfile").write_text(
        "FROM python:3.12\n",
        encoding="utf-8",
    )
    (crawler_dir / "tasks" / "owner-repo").mkdir(parents=True)
    record = {
        "repo": "owner/repo",
        "repository_url": "https://github.com/owner/repo",
        "base_commit": "abcdef123456",
        "language": "python",
        "direction": "Add streaming codec support.",
        "status": "qualified",
        "soft_score": 9,
        "taskability": {"score": 8},
        "benchmark": {"offline_ok": True, "stable": True, "test_duration_median_s": 3},
        "harbor_package": {
            "material_path": "materials/owner-repo",
            "task_path": "tasks/owner-repo",
            "harbor": {
                "template_alias": "alias",
                "template_id": "template-id",
                "launch_command": "harbor run --path tasks/owner-repo",
            },
        },
        "e2b_environment": {"runtime_version": "3.12", "execution_user": "user"},
        "test_cmd": "python -m pytest -q",
    }
    (state_dir / "candidates.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")

    records = load_candidate_records(crawler_dir)

    assert len(records) == 1
    assert has_ready_e2b_material(records[0])
    selected, warnings = select_records(records, 1)
    assert selected[0]["repo"] == "owner/repo"
    assert warnings == []

    index = prepare_materials(
        selected,
        crawler_dir=crawler_dir,
        material_dir=tmp_path / "Material",
        clone_repos=False,
        require_clone=False,
        clone_timeout_s=1,
    )

    assert index[0]["e2b"]["harbor_template_id"] == "template-id"
    assert (tmp_path / "Material" / "handoff" / "owner-repo.json").is_file()
    assert (tmp_path / "Material" / "repo-summary" / "owner-repo.summary.json").is_file()
    assert (tmp_path / "Material" / "materials" / "owner-repo" / "environment" / "Dockerfile").is_file()
    assert index[0]["clone_status"] == "skipped"
