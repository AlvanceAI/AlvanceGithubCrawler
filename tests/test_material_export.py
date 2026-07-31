from __future__ import annotations

import json

from alvance_github_crawler.material_export import (
    has_ready_e2b_material,
    load_candidate_records,
    prepare_materials,
    select_records,
)


def test_load_select_and_prepare_ready_registry_materials(tmp_path) -> None:
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
    assert (
        tmp_path / "Material" / "materials" / "owner-repo" / "environment" / "Dockerfile"
    ).is_file()
    assert index[0]["clone_status"] == "skipped"


def test_loads_xby_package_schema_with_e2b_history(tmp_path) -> None:
    crawler_dir = tmp_path / "crawler"
    catalog_dir = crawler_dir / "catalog"
    task_dir = crawler_dir / "tasks" / "owner-repo"
    material_dir = crawler_dir / "materials" / "owner-repo"
    catalog_dir.mkdir(parents=True)
    task_dir.mkdir(parents=True)
    material_dir.mkdir(parents=True)
    (task_dir / "direction.md").write_text("Improve parser diagnostics.\n", encoding="utf-8")
    (material_dir / "material.toml").write_text("schema_version = \"0.3\"\n", encoding="utf-8")
    package = {
        "schema_version": "0.3",
        "repo": "owner/repo",
        "base_commit": "abcdef123456",
        "source_tree": "tree-sha",
        "default_branch": "main",
        "license": "MIT",
        "language": "go",
        "runtime_version": "1.22.0",
        "test_cmd": "go test ./...",
        "status": "qualified",
        "material_path": "materials/owner-repo",
        "task_path": "tasks/owner-repo",
        "harbor": {"launch_command": "harbor run"},
        "e2b_history": {
            "source_template": {"alias": "go-1-22", "template_id": "source-id"},
            "harbor_template": {"alias": "task-env-1234abcd", "template_id": "harbor-id"},
        },
        "verification": {"offline_ok": True, "stable": True, "test_duration_median_s": 10},
        "quality": {
            "direction": {
                "keywords": ["parser", "diagnostics"],
                "target_paths": ["pkg/parser.go"],
            },
            "taskability": {"score": 7},
            "contamination": {"risk": "unknown"},
        },
    }
    (catalog_dir / "e2b-packages.jsonl").write_text(json.dumps(package) + "\n", encoding="utf-8")

    records = load_candidate_records(crawler_dir)

    assert len(records) == 1
    record = records[0]
    assert record["direction"] == "Improve parser diagnostics."
    assert record["direction_target_paths"] == ["pkg/parser.go"]
    assert has_ready_e2b_material(record)

    selected, _ = select_records(records, 1)
    index = prepare_materials(
        selected,
        crawler_dir=crawler_dir,
        material_dir=tmp_path / "Material",
        clone_repos=False,
        require_clone=False,
        clone_timeout_s=1,
    )

    assert index[0]["e2b"]["source_template_alias"] == "go-1-22"
    assert index[0]["e2b"]["harbor_template_alias"] == "task-env-1234abcd"
    handoff = json.loads(
        (tmp_path / "Material" / "handoff" / "owner-repo.json").read_text(encoding="utf-8")
    )
    assert handoff["e2b_template"] == "go-1-22"
    assert handoff["harbor_package"]["e2b_history"]["harbor_template"]["template_id"] == "harbor-id"
