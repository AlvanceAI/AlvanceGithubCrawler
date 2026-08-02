from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
import tomllib
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dirhash import dirhash

from ..jsonl_io import split_jsonl_lines
from ..runtime.profiles import execution_user, runtime_environment
from ..runtime.recipes import repository_dependency_commands, runtime_base_image
from ..workspace import cloned_repository
from .harbor_task import (
    render_environment_dockerfile,
    render_task_material_toml,
    render_task_toml,
    validate_e2b_dockerfile,
)
from .package_models import E2BWrapperReceipt, QualifiedRepository
from .trace_materials import (
    render_catalog,
    render_material_readme,
    render_material_toml,
)


class PackageRepairError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class RepairResult:
    package_id: str
    changed: bool
    language: str
    dependency_commands: tuple[str, ...]


def repair_packages(
    root_dir: Path,
    *,
    workers: int = 8,
    check_only: bool = False,
) -> dict[str, Any]:
    """Repair or audit every catalog package without touching validation receipts."""
    root_dir = root_dir.resolve()
    catalog_dir = root_dir / "catalog"
    catalog_path = catalog_dir / "e2b-packages.jsonl"
    if not catalog_path.is_file():
        raise PackageRepairError(f"package catalog does not exist: {catalog_path}")

    records = _load_records(catalog_path)
    if not records:
        raise PackageRepairError("package catalog is empty")

    workers = max(1, min(int(workers), 20))
    command_map = _resolve_missing_commands(records, workers=workers)
    results: list[RepairResult] = []
    repaired_records: list[dict[str, Any]] = []
    for record in records:
        result, repaired = _repair_one(
            root_dir,
            record,
            dependency_commands=command_map.get(str(record["package_id"])),
            check_only=check_only,
        )
        results.append(result)
        repaired_records.append(repaired)

    audit_errors = _audit(root_dir, repaired_records)
    if audit_errors:
        details = "\n".join(f"- {item}" for item in audit_errors[:40])
        raise PackageRepairError(
            f"package repair audit failed with {len(audit_errors)} issue(s):\n{details}"
        )

    changed = sum(item.changed for item in results)
    if not check_only:
        _atomic_write(
            catalog_path,
            "".join(
                json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n"
                for item in sorted(repaired_records, key=lambda value: str(value["package_id"]))
            ),
        )
        _atomic_write(
            catalog_dir / "repo-materials.toml",
            render_catalog(repaired_records),
        )

    by_language: dict[str, int] = {}
    for item in results:
        by_language[item.language] = by_language.get(item.language, 0) + 1
    return {
        "checked": len(results),
        "changed": changed,
        "unchanged": len(results) - changed,
        "python_dependency_resolutions": sum(
            1 for package_id in command_map if _record_language(records, package_id) == "python"
        ),
        "languages": dict(sorted(by_language.items())),
        "mode": "check" if check_only else "repair",
    }


def _record_language(records: list[dict[str, Any]], package_id: str) -> str:
    for record in records:
        if str(record.get("package_id")) == package_id:
            return str(record.get("language") or "").lower()
    return ""


def _load_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    lines = split_jsonl_lines(path.read_text(encoding="utf-8"))
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise PackageRepairError(f"invalid JSON at {path}:{line_number}") from exc
        if not isinstance(record, dict) or not record.get("package_id"):
            raise PackageRepairError(f"invalid package record at {path}:{line_number}")
        package_id = str(record["package_id"])
        if package_id in seen:
            raise PackageRepairError(f"duplicate package_id in catalog: {package_id}")
        seen.add(package_id)
        records.append(record)
    return records


def _resolve_missing_commands(
    records: list[dict[str, Any]],
    *,
    workers: int,
) -> dict[str, tuple[str, ...]]:
    missing = [
        record
        for record in records
        if not _stored_commands(record) and str(record.get("language") or "").lower() == "python"
    ]
    if not missing:
        return {}

    resolved: dict[str, tuple[str, ...]] = {}
    errors: list[str] = []

    def resolve(record: dict[str, Any]) -> tuple[str, tuple[str, ...]]:
        package_id = str(record["package_id"])
        repo = str(record.get("repo") or "")
        commit = str(record.get("base_commit") or "")
        if not repo or not commit:
            raise PackageRepairError(f"{package_id}: missing repository or commit")
        with cloned_repository(repo, commit) as repo_path:
            return package_id, repository_dependency_commands("python", repo_path)

    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="repair-python") as pool:
        futures = {pool.submit(resolve, record): record for record in missing}
        for future in as_completed(futures):
            record = futures[future]
            try:
                package_id, commands = future.result()
            except Exception as exc:
                errors.append(f"{record.get('package_id')}: {type(exc).__name__}: {exc}")
            else:
                resolved[package_id] = commands
    if errors:
        details = "\n".join(f"- {item}" for item in sorted(errors))
        raise PackageRepairError(f"could not resolve Python build recipes:\n{details}")
    return resolved


def _stored_commands(record: dict[str, Any]) -> tuple[str, ...]:
    raw = record.get("dependency_commands")
    if not isinstance(raw, list):
        return ()
    return tuple(str(item) for item in raw if str(item).strip())


def _repair_one(
    root_dir: Path,
    original: dict[str, Any],
    *,
    dependency_commands: tuple[str, ...] | None,
    check_only: bool,
) -> tuple[RepairResult, dict[str, Any]]:
    record = json.loads(json.dumps(original))
    package_id = str(record["package_id"])
    language = str(record.get("language") or "").lower()
    commands = (
        _stored_commands(record)
        or dependency_commands
        or repository_dependency_commands(language)
    )
    repository = _repository_from_record(record, commands)
    task_path = _safe_path(root_dir, str(record.get("task_path") or ""))
    material_path = _safe_path(root_dir, str(record.get("material_path") or ""))
    task_environment = task_path / "environment"
    material_environment = material_path / "environment"
    if not task_environment.is_dir() or not material_environment.is_dir():
        raise PackageRepairError(f"{package_id}: missing environment directory")

    dockerfile = render_environment_dockerfile(repository)
    new_hash = _environment_hash(task_environment, dockerfile)
    old_hash = str(record.get("environment_sha256") or "")
    changed = (
        (task_environment / "Dockerfile").read_text(encoding="utf-8", errors="replace")
        != dockerfile
        or (material_environment / "Dockerfile").read_text(
            encoding="utf-8", errors="replace"
        )
        != dockerfile
        or old_hash != new_hash
        or not _is_rebuildable_record(record)
    )

    repaired = _rewrite_record_metadata(record, repository, new_hash)
    if check_only:
        return RepairResult(package_id, changed, language, commands), repaired

    _atomic_write(task_environment / "Dockerfile", dockerfile)
    _atomic_write(material_environment / "Dockerfile", dockerfile)
    _atomic_write(
        task_path / "task.toml",
        render_task_toml(repository, task_path.name, material_path.name),
    )
    history = repaired["e2b_history"]
    wrapper = E2BWrapperReceipt(
        source_template_id=str(history["source_template"].get("template_id") or "historical"),
        harbor_template_id=str(history["harbor_template"].get("template_id") or "historical"),
        harbor_template_alias=str(history["harbor_template"].get("alias") or "historical"),
        cache_hit=True,
        build_duration_s=0.0,
        smoke=dict((repaired.get("harbor") or {}).get("smoke") or {}),
    )
    _atomic_write(
        material_path / "material.toml",
        render_material_toml(
            repository,
            material_id=material_path.name,
            environment_sha256=new_hash,
            wrapper=wrapper,
        ),
    )
    _atomic_write(
        material_path / "README.md",
        render_material_readme(repository, material_path.name),
    )
    _atomic_write(
        task_path / "material.toml",
        render_task_material_toml(
            repository,
            material=material_path.name,
            material_path=str(record["material_path"]),
            environment_sha256=new_hash,
            template_id=wrapper.harbor_template_id,
            template_alias=wrapper.harbor_template_alias,
        ),
    )
    return RepairResult(package_id, changed, language, commands), repaired


def _repository_from_record(
    record: dict[str, Any],
    dependency_commands: tuple[str, ...],
) -> QualifiedRepository:
    language = str(record.get("language") or "").lower()
    runtime_version = str(record.get("runtime_version") or "")
    if not runtime_version:
        raise PackageRepairError(f"{record.get('package_id')}: missing runtime_version")
    history = record.get("e2b_history") or {}
    source = history.get("source_template") or record.get("source_template") or {}
    source_alias = str(source.get("alias") or source.get("template_id") or "historical")
    resources = record.get("resources") or {}
    return QualifiedRepository(
        repo=str(record.get("repo") or ""),
        base_commit=str(record.get("base_commit") or ""),
        source_tree=str(record.get("source_tree") or ""),
        default_branch=str(record.get("default_branch") or "main"),
        license=str(record.get("license") or "NOASSERTION"),
        language=language,
        runtime_version=runtime_version,
        test_cmd=str(record.get("test_cmd") or ""),
        direction="",
        source_template_alias=source_alias,
        dependency_commands=dependency_commands,
        runtime_env=dict(
            record.get("runtime_env") or runtime_environment(language, runtime_version)
        ),
        execution_user=str(record.get("execution_user") or execution_user(language)),
        cpu_count=int(resources.get("cpu_count") or 1),
        memory_mb=int(resources.get("memory_mb") or 1_024),
    )


def _rewrite_record_metadata(
    record: dict[str, Any],
    repository: QualifiedRepository,
    environment_sha256: str,
) -> dict[str, Any]:
    old_source = record.get("source_template") or {}
    old_harbor = record.get("harbor") or {}
    history = record.get("e2b_history") or {}
    source_history = history.get("source_template") or old_source
    harbor_history = history.get("harbor_template") or {
        "alias": old_harbor.get("template_alias", ""),
        "template_id": old_harbor.get("template_id", ""),
    }
    history = {
        "source_template": dict(source_history),
        "harbor_template": dict(harbor_history),
        "validation_environment_sha256": str(
            history.get("validation_environment_sha256")
            or record.get("environment_sha256")
            or ""
        ),
    }
    record.pop("source_template", None)
    record["schema_version"] = "0.3"
    record["dependency_commands"] = list(repository.dependency_commands)
    record["environment_sha256"] = environment_sha256
    record["e2b_history"] = history
    harbor = dict(record.get("harbor") or {})
    harbor.pop("template_alias", None)
    harbor.pop("template_id", None)
    harbor["build_source"] = "environment/Dockerfile"
    harbor["dockerfile_rebuildable"] = True
    record["harbor"] = harbor
    storage = dict(record.get("storage") or {})
    storage.update(
        {
            "remote_e2b_only": False,
            "dockerfile_rebuildable": True,
            "rebuild_network_required": True,
        }
    )
    record["storage"] = storage
    return record


def _is_rebuildable_record(record: dict[str, Any]) -> bool:
    storage = record.get("storage") or {}
    harbor = record.get("harbor") or {}
    return bool(
        record.get("dependency_commands")
        and storage.get("dockerfile_rebuildable") is True
        and storage.get("remote_e2b_only") is False
        and harbor.get("dockerfile_rebuildable") is True
    )


def _environment_hash(environment_dir: Path, dockerfile: str) -> str:
    with tempfile.TemporaryDirectory(prefix="alvance-environment-repair-") as temp_dir:
        copied = Path(temp_dir) / "environment"
        shutil.copytree(environment_dir, copied)
        (copied / "Dockerfile").write_text(dockerfile, encoding="utf-8")
        return dirhash(copied, "sha256")


def _safe_path(root_dir: Path, relative: str) -> Path:
    if not relative:
        raise PackageRepairError("package record has an empty path")
    path = (root_dir / relative).resolve()
    if not path.is_relative_to(root_dir):
        raise PackageRepairError(f"package path escapes repository: {relative}")
    return path


def _audit(root_dir: Path, records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for record in records:
        package_id = str(record.get("package_id") or "unknown")
        try:
            task = _safe_path(root_dir, str(record.get("task_path") or ""))
            material = _safe_path(root_dir, str(record.get("material_path") or ""))
        except PackageRepairError as exc:
            errors.append(f"{package_id}: {exc}")
            continue
        task_dockerfile = task / "environment" / "Dockerfile"
        material_dockerfile = material / "environment" / "Dockerfile"
        if not task_dockerfile.is_file() or not material_dockerfile.is_file():
            errors.append(f"{package_id}: Dockerfile missing")
            continue
        task_content = task_dockerfile.read_text(encoding="utf-8", errors="replace")
        material_content = material_dockerfile.read_text(encoding="utf-8", errors="replace")
        if task_content != material_content:
            errors.append(f"{package_id}: task/material Dockerfiles differ")
        try:
            validate_e2b_dockerfile(task_content)
        except ValueError as exc:
            errors.append(f"{package_id}: {exc}")
        if "FROM e2bdev/base" in task_content:
            errors.append(f"{package_id}: E2B fingerprint Dockerfile remains")
        commit = str(record.get("base_commit") or "")
        tree = str(record.get("source_tree") or "")
        if commit and commit not in task_content:
            errors.append(f"{package_id}: base commit absent from Dockerfile")
        if tree and tree not in task_content:
            errors.append(f"{package_id}: source tree absent from Dockerfile")
        if "git submodule update --init --recursive" not in task_content:
            errors.append(f"{package_id}: recursive submodule initialization absent")
        language = str(record.get("language") or "").lower()
        runtime_version = str(record.get("runtime_version") or "")
        try:
            expected_image = f"FROM {runtime_base_image(language, runtime_version)}"
        except ValueError as exc:
            errors.append(f"{package_id}: {exc}")
        else:
            if expected_image not in task_content:
                errors.append(f"{package_id}: expected runtime image absent")
        commands = _stored_commands(record)
        for command in commands:
            if command not in task_content:
                errors.append(f"{package_id}: setup command absent: {command}")
        storage = record.get("storage") or {}
        if storage.get("remote_e2b_only") is not False:
            errors.append(f"{package_id}: remote_e2b_only is not false")
        if storage.get("dockerfile_rebuildable") is not True:
            errors.append(f"{package_id}: dockerfile_rebuildable flag missing")
        if storage.get("rebuild_network_required") is not True:
            errors.append(f"{package_id}: rebuild_network_required flag missing")
        if "source_template" in record:
            errors.append(f"{package_id}: source template remains operational metadata")
        harbor = record.get("harbor") or {}
        if "template_alias" in harbor or "template_id" in harbor:
            errors.append(f"{package_id}: Harbor template remains operational metadata")
        if not record.get("e2b_history"):
            errors.append(f"{package_id}: E2B validation history missing")
        actual_hash = dirhash(task / "environment", "sha256")
        if actual_hash != str(record.get("environment_sha256") or ""):
            errors.append(f"{package_id}: current environment hash mismatch")
        _audit_toml(package_id, task, material, errors)
        if task_content.startswith("# Harbor envelope v2\n# Source E2B template:"):
            errors.append(f"{package_id}: legacy fingerprint header remains")
    return errors


def _audit_toml(
    package_id: str,
    task: Path,
    material: Path,
    errors: list[str],
) -> None:
    try:
        with (task / "task.toml").open("rb") as handle:
            task_config = tomllib.load(handle)
        with (task / "material.toml").open("rb") as handle:
            task_material = tomllib.load(handle)
        with (material / "material.toml").open("rb") as handle:
            material_config = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        errors.append(f"{package_id}: invalid package TOML: {exc}")
        return

    metadata = task_config.get("metadata") or {}
    if metadata.get("storage_mode") != "dockerfile-rebuildable":
        errors.append(f"{package_id}: task storage_mode is not rebuildable")
    if metadata.get("dockerfile_rebuildable") is not True:
        errors.append(f"{package_id}: task rebuildable flag missing")
    environment = material_config.get("environment") or {}
    if environment.get("mode") != "dockerfile-rebuildable":
        errors.append(f"{package_id}: material environment mode is not rebuildable")
    if environment.get("dockerfile_rebuildable") is not True:
        errors.append(f"{package_id}: material rebuildable flag missing")
    operational_e2b_fields = {
        "harbor_template_alias",
        "e2b_template",
        "source_template_alias",
        "source_template_id",
    }
    if operational_e2b_fields.intersection(environment):
        errors.append(f"{package_id}: material retains operational E2B fields")
    if "e2b_history" not in material_config:
        errors.append(f"{package_id}: material E2B history missing")
    if task_material.get("dockerfile_rebuildable") is not True:
        errors.append(f"{package_id}: task material rebuildable flag missing")
    if {"e2b_template_id", "e2b_template_alias"}.intersection(task_material):
        errors.append(f"{package_id}: task material retains operational E2B fields")


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.repair-{os.getpid()}")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Repair and audit rebuildable Harbor packages")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--check", action="store_true", help="audit without writing files")
    args = parser.parse_args(argv)
    try:
        result = repair_packages(args.root, workers=args.workers, check_only=args.check)
    except PackageRepairError as exc:
        print(str(exc))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
