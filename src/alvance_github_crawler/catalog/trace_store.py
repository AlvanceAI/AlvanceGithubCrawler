from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from .harbor_task import (
    harbor_template_alias,
    material_id,
    render_environment_dockerfile,
    render_instruction,
    render_task_material_toml,
    render_task_toml,
    render_test_script,
    task_name,
)
from .package_models import (
    E2BWrapperReceipt,
    PreparedTracePackage,
    QualifiedRepository,
)
from .trace_materials import (
    build_e2b_receipt,
    render_baseline_script,
    render_catalog,
    render_export_patch_script,
    render_material_readme,
    render_material_toml,
)


class TracePackageStore:
    """Persist immutable Trace catalog, material, and Harbor task records."""

    def __init__(self, catalog_dir: Path) -> None:
        self.catalog_dir = catalog_dir
        self.root_dir = catalog_dir.parent
        self.materials_dir = self.root_dir / "materials"
        self.tasks_dir = self.root_dir / "tasks"

    def prepare(self, repository: QualifiedRepository) -> PreparedTracePackage:
        material = material_id(repository)
        task = task_name(repository)
        material_dir = self.materials_dir / material
        task_dir = self.tasks_dir / task
        material_environment = material_dir / "environment"
        task_environment = task_dir / "environment"
        material_environment.mkdir(parents=True, exist_ok=True)
        task_environment.mkdir(parents=True, exist_ok=True)

        dockerfile = render_environment_dockerfile(repository)
        (material_environment / "Dockerfile").write_text(dockerfile, encoding="utf-8")
        (task_environment / "Dockerfile").write_text(dockerfile, encoding="utf-8")

        alias = harbor_template_alias(task, task_environment)
        environment_sha256 = alias.rsplit("-env-", 1)[-1]
        try:
            from dirhash import dirhash
        except ImportError as exc:
            raise RuntimeError("dirhash is required for Trace packaging") from exc
        full_environment_hash = dirhash(task_environment, "sha256")
        if not full_environment_hash.startswith(environment_sha256):
            raise RuntimeError("Harbor environment hash is inconsistent")

        return PreparedTracePackage(
            material_id=material,
            task_name=task,
            material_path=material_dir.relative_to(self.root_dir).as_posix(),
            task_path=task_dir.relative_to(self.root_dir).as_posix(),
            environment_sha256=full_environment_hash,
            harbor_template_alias=alias,
        )

    def finalize(
        self,
        repository: QualifiedRepository,
        prepared: PreparedTracePackage,
        wrapper: E2BWrapperReceipt,
        package_record: dict[str, Any],
    ) -> None:
        material_dir = self.root_dir / prepared.material_path
        task_dir = self.root_dir / prepared.task_path
        self._write_material(repository, prepared, wrapper, material_dir)
        self._write_task(repository, prepared, wrapper, task_dir)
        packages = self._upsert_package(package_record)
        (self.catalog_dir / "repo-materials.toml").write_text(
            render_catalog(packages),
            encoding="utf-8",
        )

    def _write_material(
        self,
        repository: QualifiedRepository,
        prepared: PreparedTracePackage,
        wrapper: E2BWrapperReceipt,
        material_dir: Path,
    ) -> None:
        scripts_dir = material_dir / "scripts"
        receipts_dir = material_dir / "receipts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        receipts_dir.mkdir(parents=True, exist_ok=True)
        (material_dir / "material.toml").write_text(
            render_material_toml(
                repository,
                material_id=prepared.material_id,
                environment_sha256=prepared.environment_sha256,
                wrapper=wrapper,
            ),
            encoding="utf-8",
        )
        (material_dir / "README.md").write_text(
            render_material_readme(repository, prepared.material_id),
            encoding="utf-8",
        )
        baseline = scripts_dir / "baseline.sh"
        baseline.write_text(render_baseline_script(repository), encoding="utf-8")
        baseline.chmod(0o755)
        export_patch = scripts_dir / "export-patch.sh"
        export_patch.write_text(render_export_patch_script(repository), encoding="utf-8")
        export_patch.chmod(0o755)
        receipt = build_e2b_receipt(
            repository,
            environment_sha256=prepared.environment_sha256,
            wrapper=wrapper,
        )
        (receipts_dir / "e2b.json").write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def _write_task(
        self,
        repository: QualifiedRepository,
        prepared: PreparedTracePackage,
        wrapper: E2BWrapperReceipt,
        task_dir: Path,
    ) -> None:
        tests_dir = task_dir / "tests"
        solution_dir = task_dir / "solution"
        tests_dir.mkdir(parents=True, exist_ok=True)
        solution_dir.mkdir(parents=True, exist_ok=True)
        instruction = render_instruction(repository)
        (task_dir / "direction.md").write_text(repository.direction + "\n", encoding="utf-8")
        (task_dir / "instruction.md").write_text(instruction, encoding="utf-8")
        (task_dir / "task.toml").write_text(
            render_task_toml(repository, prepared.task_name, prepared.material_id),
            encoding="utf-8",
        )
        (task_dir / "material.toml").write_text(
            render_task_material_toml(
                repository,
                material=prepared.material_id,
                material_path=prepared.material_path,
                environment_sha256=prepared.environment_sha256,
                template_id=wrapper.harbor_template_id,
                template_alias=wrapper.harbor_template_alias,
            ),
            encoding="utf-8",
        )
        test_path = tests_dir / "test.sh"
        test_path.write_text(render_test_script(repository), encoding="utf-8")
        test_path.chmod(0o755)
        solve_path = solution_dir / "solve.sh"
        solve_path.write_text("#!/bin/sh\nset -eu\nexit 0\n", encoding="utf-8")
        solve_path.chmod(0o755)

    def _upsert_package(self, package: dict[str, Any]) -> list[dict[str, Any]]:
        self.catalog_dir.mkdir(parents=True, exist_ok=True)
        path = self.catalog_dir / "e2b-packages.jsonl"
        packages: dict[str, dict[str, Any]] = {}
        if path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                try:
                    existing = json.loads(line)
                except json.JSONDecodeError:
                    continue
                package_id = str(existing.get("package_id") or "")
                if package_id and existing.get("material_id"):
                    packages[package_id] = existing
        packages[str(package["package_id"])] = package
        ordered = [packages[key] for key in sorted(packages)]
        payload = "".join(
            json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in ordered
        )
        path.write_text(payload, encoding="utf-8")
        return ordered

    def remove_task(self, task: str) -> None:
        shutil.rmtree(self.tasks_dir / task, ignore_errors=True)
