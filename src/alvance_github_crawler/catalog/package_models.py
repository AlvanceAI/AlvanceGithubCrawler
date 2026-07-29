from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from ..runtime.profiles import execution_user, runtime_environment

PACKAGE_SCHEMA_VERSION = "0.2"


@dataclass(frozen=True, slots=True)
class QualifiedRepository:
    repo: str
    base_commit: str
    source_tree: str
    default_branch: str
    license: str
    language: str
    runtime_version: str
    test_cmd: str
    direction: str
    source_template_alias: str
    runtime_env: dict[str, str]
    execution_user: str
    cpu_count: int = 1
    memory_mb: int = 1_024

    @property
    def repository_url(self) -> str:
        return f"https://github.com/{self.repo}"

    @classmethod
    def from_candidate(cls, record: dict[str, Any]) -> QualifiedRepository:
        environment = record.get("e2b_environment") or {}
        required = {
            "repo": record.get("repo"),
            "base_commit": record.get("base_commit"),
            "source_tree": record.get("source_tree"),
            "language": record.get("language"),
            "runtime_version": environment.get("runtime_version"),
            "test_cmd": record.get("test_cmd"),
            "source_template_alias": record.get("e2b_template"),
        }
        missing = [key for key, value in required.items() if not value]
        if missing:
            raise ValueError(f"candidate is missing package fields: {', '.join(missing)}")
        language = str(required["language"]).lower()
        runtime_version = str(required["runtime_version"])
        return cls(
            repo=str(required["repo"]),
            base_commit=str(required["base_commit"]),
            source_tree=str(required["source_tree"]),
            default_branch=str(record.get("default_branch") or "main"),
            license=str(record.get("license") or "NOASSERTION"),
            language=language,
            runtime_version=runtime_version,
            test_cmd=str(required["test_cmd"]),
            direction=str(record.get("direction") or ""),
            source_template_alias=str(required["source_template_alias"]),
            runtime_env=runtime_environment(language, runtime_version),
            execution_user=str(environment.get("execution_user") or execution_user(language)),
            cpu_count=int(environment.get("cpu_count") or 1),
            memory_mb=int(environment.get("memory_mb") or 1_024),
        )


@dataclass(frozen=True, slots=True)
class PreparedTracePackage:
    material_id: str
    task_name: str
    material_path: str
    task_path: str
    environment_sha256: str
    harbor_template_alias: str


@dataclass(frozen=True, slots=True)
class E2BWrapperReceipt:
    source_template_id: str
    harbor_template_id: str
    harbor_template_alias: str
    cache_hit: bool
    build_duration_s: float
    smoke: dict[str, Any]


@dataclass(frozen=True, slots=True)
class HarborPackageResult:
    package_id: str
    material_id: str
    task_name: str
    material_path: str
    task_path: str
    source_template_alias: str
    source_template_id: str
    harbor_template_alias: str
    harbor_template_id: str
    wrapper_cache_hit: bool
    wrapper_build_s: float
    smoke_ok: bool
    launch_command: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def compact_package_record(
    candidate_record: dict[str, Any],
    repository: QualifiedRepository,
    prepared: PreparedTracePackage,
    wrapper: E2BWrapperReceipt,
    result: HarborPackageResult,
) -> dict[str, Any]:
    environment = candidate_record.get("e2b_environment") or {}
    offline = environment.get("offline") or {}
    benchmark = candidate_record.get("benchmark") or {}
    return {
        "schema_version": PACKAGE_SCHEMA_VERSION,
        "package_id": result.package_id,
        "material_id": result.material_id,
        "status": "qualified",
        "repo": repository.repo,
        "repository_url": repository.repository_url,
        "base_commit": repository.base_commit,
        "source_tree": repository.source_tree,
        "default_branch": repository.default_branch,
        "license": repository.license,
        "language": repository.language,
        "runtime_version": repository.runtime_version,
        "runtime_env": repository.runtime_env,
        "workdir": "/app",
        "test_cmd": repository.test_cmd,
        "execution_user": repository.execution_user,
        "resources": {
            "cpu_count": repository.cpu_count,
            "memory_mb": repository.memory_mb,
        },
        "material_path": prepared.material_path,
        "task_path": prepared.task_path,
        "environment_sha256": prepared.environment_sha256,
        "source_template": {
            "alias": repository.source_template_alias,
            "template_id": wrapper.source_template_id,
        },
        "harbor": {
            "task_name": result.task_name,
            "template_alias": result.harbor_template_alias,
            "template_id": result.harbor_template_id,
            "launch_command": result.launch_command,
            "smoke": wrapper.smoke,
        },
        "verification": {
            "offline_ok": offline.get("ok"),
            "offline_duration_s": offline.get("duration_s"),
            "cold_start_median_s": benchmark.get("cold_start_median_s"),
            "test_duration_median_s": benchmark.get("test_duration_median_s"),
            "peak_mem_median_mb": benchmark.get("peak_mem_median_mb"),
            "stable": benchmark.get("stable"),
        },
        "storage": {
            "local_source": False,
            "local_image": False,
            "local_build_cache": False,
            "remote_e2b_only": True,
        },
    }
