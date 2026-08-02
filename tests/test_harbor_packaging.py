from __future__ import annotations

import json
import tomllib

import pytest

from alvance_github_crawler.catalog.harbor_task import (
    render_environment_dockerfile,
    validate_e2b_dockerfile,
)
from alvance_github_crawler.catalog.package_models import (
    E2BWrapperReceipt,
    HarborPackageResult,
    QualifiedRepository,
    compact_package_record,
)
from alvance_github_crawler.catalog.trace_store import TracePackageStore


def candidate_record() -> dict[str, object]:
    return {
        "repo": "owner/example-repository",
        "base_commit": "a" * 40,
        "source_tree": "b" * 40,
        "default_branch": "main",
        "license": "MIT",
        "language": "python",
        "test_cmd": "python -m pytest -q",
        "direction": "Add the requested feature.",
        "e2b_template": "source-template-v7",
        "e2b_environment": {
            "runtime_version": "3.12",
            "offline": {
                "ok": True,
                "duration_s": 1.0,
                "stdout_tail": "large log",
            },
        },
        "benchmark": {
            "cold_start_median_s": 0.5,
            "test_duration_median_s": 2.0,
            "peak_mem_median_mb": 100.0,
            "stable": True,
        },
    }


def test_durable_dockerfile_uses_only_e2b_supported_instructions() -> None:
    repository = QualifiedRepository.from_candidate(candidate_record())

    dockerfile = render_environment_dockerfile(repository)

    assert not any(line.lstrip().startswith("#") for line in dockerfile.splitlines())
    validate_e2b_dockerfile(dockerfile)


def test_e2b_dockerfile_contract_rejects_comment_nodes() -> None:
    with pytest.raises(ValueError, match=r"instruction\(s\): COMMENT"):
        validate_e2b_dockerfile("# metadata\nFROM python:3.12\n")


def test_trace_store_writes_tiny_native_layout(tmp_path) -> None:
    record = candidate_record()
    repository = QualifiedRepository.from_candidate(record)
    store = TracePackageStore(tmp_path / "catalog")
    prepared = store.prepare(repository)
    wrapper = E2BWrapperReceipt(
        source_template_id="source-id",
        harbor_template_id="harbor-id",
        harbor_template_alias=prepared.harbor_template_alias,
        cache_hit=False,
        build_duration_s=2.0,
        smoke={
            "ok": True,
            "base_commit": repository.base_commit,
            "sandbox_destroyed": True,
        },
    )
    result = HarborPackageResult(
        package_id=prepared.material_id,
        material_id=prepared.material_id,
        task_name=prepared.task_name,
        material_path=prepared.material_path,
        task_path=prepared.task_path,
        source_template_alias=repository.source_template_alias,
        source_template_id=wrapper.source_template_id,
        harbor_template_alias=wrapper.harbor_template_alias,
        harbor_template_id=wrapper.harbor_template_id,
        wrapper_cache_hit=False,
        wrapper_build_s=2.0,
        smoke_ok=True,
        launch_command="harbor run",
    )
    package = compact_package_record(record, repository, prepared, wrapper, result)
    store.finalize(repository, prepared, wrapper, package)

    material_dir = tmp_path / prepared.material_path
    task_dir = tmp_path / prepared.task_path
    assert (tmp_path / "catalog" / "repo-materials.toml").is_file()
    assert (material_dir / "material.toml").is_file()
    assert (material_dir / "receipts" / "e2b.json").is_file()
    assert (task_dir / "material.toml").is_file()
    assert (task_dir / "direction.md").is_file()
    assert "WORKDIR /app" in (task_dir / "environment" / "Dockerfile").read_text()
    test_script = (task_dir / "tests" / "test.sh").read_text()
    assert "cd /app" in test_script
    assert "runuser -u user -- env HOME=/home/user" in test_script
    assert "echo 1 > /logs/verifier/reward.txt" in test_script
    assert "echo 0 > /logs/verifier/reward.txt" in test_script
    task_config = (task_dir / "task.toml").read_text()
    assert "cpus = 1" in task_config
    assert "memory_mb = 1024" in task_config
    assert not any(path.name == ".git" for path in tmp_path.rglob(".git"))
    assert sum(path.stat().st_size for path in tmp_path.rglob("*") if path.is_file()) < 30_000

    with (material_dir / "material.toml").open("rb") as handle:
        material = tomllib.load(handle)
    assert material["environment"]["mode"] == "dockerfile-rebuildable"
    assert material["environment"]["dockerfile_rebuildable"] is True
    assert material["e2b_history"]["template_id"] == "harbor-id"
    assert material["e2b_history"]["operational_dependency"] is False
    assert material["source"]["source_tree"] == "b" * 40
    assert (
        "runuser -u user -- env HOME=/home/user"
        in (material_dir / "scripts" / "baseline.sh").read_text()
    )
    receipt = json.loads((material_dir / "receipts" / "e2b.json").read_text())
    assert receipt["execution_user"] == "user"
    assert receipt["resources"] == {"cpu_count": 1, "memory_mb": 1024}


def test_compact_package_omits_test_logs(tmp_path) -> None:
    record = candidate_record()
    repository = QualifiedRepository.from_candidate(record)
    prepared = TracePackageStore(tmp_path / "catalog").prepare(repository)
    wrapper = E2BWrapperReceipt(
        source_template_id="source-id",
        harbor_template_id="harbor-id",
        harbor_template_alias=prepared.harbor_template_alias,
        cache_hit=True,
        build_duration_s=0.0,
        smoke={"ok": True, "sandbox_destroyed": True},
    )
    result = HarborPackageResult(
        package_id=prepared.material_id,
        material_id=prepared.material_id,
        task_name=prepared.task_name,
        material_path=prepared.material_path,
        task_path=prepared.task_path,
        source_template_alias=repository.source_template_alias,
        source_template_id="source-id",
        harbor_template_alias=prepared.harbor_template_alias,
        harbor_template_id="harbor-id",
        wrapper_cache_hit=True,
        wrapper_build_s=0.0,
        smoke_ok=True,
        launch_command="harbor run",
    )
    payload = compact_package_record(record, repository, prepared, wrapper, result)
    serialized = json.dumps(payload)
    assert "large log" not in serialized
    assert payload["storage"]["remote_e2b_only"] is False
    assert payload["storage"]["dockerfile_rebuildable"] is True
    assert payload["harbor"]["build_source"] == "environment/Dockerfile"
    assert payload["e2b_history"]["harbor_template"]["template_id"] == "harbor-id"
    assert payload["execution_user"] == "user"
