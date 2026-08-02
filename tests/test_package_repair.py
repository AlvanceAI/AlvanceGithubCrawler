from __future__ import annotations

import json
from pathlib import Path

from alvance_github_crawler.catalog.harbor_packaging import HarborPackageResult
from alvance_github_crawler.catalog.package_models import (
    E2BWrapperReceipt,
    QualifiedRepository,
    compact_package_record,
)
from alvance_github_crawler.catalog.package_repair import repair_packages
from alvance_github_crawler.catalog.trace_store import TracePackageStore


def _go_candidate() -> dict[str, object]:
    return {
        "repo": "owner/example-repository",
        "base_commit": "a" * 40,
        "source_tree": "b" * 40,
        "default_branch": "main",
        "license": "MIT",
        "language": "go",
        "test_cmd": "go test ./...",
        "direction": "Add the requested feature.",
        "e2b_template": "source-template-v7",
        "e2b_environment": {"runtime_version": "1.22.0"},
    }


def test_package_repair_is_idempotent(tmp_path: Path) -> None:
    candidate = _go_candidate()
    repository = QualifiedRepository.from_candidate(candidate)
    store = TracePackageStore(tmp_path / "catalog")
    prepared = store.prepare(repository)
    wrapper = E2BWrapperReceipt(
        source_template_id="source-id",
        harbor_template_id="harbor-id",
        harbor_template_alias=prepared.harbor_template_alias,
        cache_hit=False,
        build_duration_s=1.0,
        smoke={"ok": True, "base_commit": repository.base_commit},
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
        wrapper_cache_hit=False,
        wrapper_build_s=1.0,
        smoke_ok=True,
        launch_command="harbor run",
    )
    package = compact_package_record(candidate, repository, prepared, wrapper, result)
    catalog_path = tmp_path / "catalog" / "e2b-packages.jsonl"
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    catalog_path.write_text(json.dumps(package) + "\n", encoding="utf-8")

    old_dockerfile = (
        "# Harbor envelope v2\n"
        "# Source E2B template: source-template-v7\n"
        "FROM e2bdev/base\nUSER root\nWORKDIR /app\n"
    )
    task_environment = tmp_path / prepared.task_path / "environment" / "Dockerfile"
    material_environment = tmp_path / prepared.material_path / "environment" / "Dockerfile"
    task_environment.write_text(old_dockerfile, encoding="utf-8")
    material_environment.write_text(old_dockerfile, encoding="utf-8")

    legacy = dict(package)
    legacy.pop("dependency_commands", None)
    legacy.pop("e2b_history", None)
    legacy["source_template"] = package["e2b_history"]["source_template"]
    legacy["harbor"]["template_alias"] = package["e2b_history"]["harbor_template"]["alias"]
    legacy["harbor"]["template_id"] = package["e2b_history"]["harbor_template"]["template_id"]
    legacy["storage"] = {"remote_e2b_only": True}
    catalog_path.write_text(json.dumps(legacy) + "\n", encoding="utf-8")

    repaired = repair_packages(tmp_path, workers=1)
    assert repaired["checked"] == 1
    assert repaired["changed"] == 1
    repaired_dockerfile = task_environment.read_text(encoding="utf-8")
    assert "FROM e2bdev/base" not in repaired_dockerfile
    assert not any(line.lstrip().startswith("#") for line in repaired_dockerfile.splitlines())
    assert repaired_dockerfile == material_environment.read_text(encoding="utf-8")

    checked = repair_packages(tmp_path, workers=1, check_only=True)
    assert checked["checked"] == 1
    assert checked["changed"] == 0
    assert checked["unchanged"] == 1
