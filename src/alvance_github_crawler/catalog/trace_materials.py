from __future__ import annotations

import json
import shlex
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from typing import Any

from ..runtime.profiles import command_as_user, command_with_environment
from .package_models import E2BWrapperReceipt, QualifiedRepository

TRACE_MATERIAL_SCHEMA_VERSION = "0.2"


def render_material_toml(
    repository: QualifiedRepository,
    *,
    material_id: str,
    environment_sha256: str,
    wrapper: E2BWrapperReceipt,
) -> str:
    runtime_key = {
        "go": "go",
        "python": "python",
        "typescript": "node",
        "javascript": "node",
        "rust": "rust",
    }[repository.language]
    return f'''schema_version = "{TRACE_MATERIAL_SCHEMA_VERSION}"
material_id = {_toml_string(material_id)}
status = "qualified"

[source]
repository_url = {_toml_string(repository.repository_url)}
base_commit = {_toml_string(repository.base_commit)}
source_tree = {_toml_string(repository.source_tree)}
default_branch = {_toml_string(repository.default_branch)}
license = {_toml_string(repository.license)}

[toolchain]
language = {_toml_string(repository.language)}
{runtime_key} = {_toml_string(repository.runtime_version)}

[environment]
mode = "e2b-only"
dockerfile = "environment/Dockerfile"
workdir = "/app"
environment_sha256 = {_toml_string(environment_sha256)}
harbor_template_alias = {_toml_string(wrapper.harbor_template_alias)}
e2b_template = {_toml_string(wrapper.harbor_template_id)}
e2b_status = "ready"
e2b_receipt = "receipts/e2b.json"
source_template_alias = {_toml_string(repository.source_template_alias)}
source_template_id = {_toml_string(wrapper.source_template_id)}

[baseline]
script = "scripts/baseline.sh"
receipt = "receipts/e2b.json"

[submission]
script = "scripts/export-patch.sh"
artifact = "/logs/artifacts/model.patch"
'''


def render_material_readme(repository: QualifiedRepository, material_id: str) -> str:
    return f"""# {material_id}

Immutable E2B-only repository material for `{repository.repo}` at
`{repository.base_commit}`. Source, dependency caches, compiler caches, and images are
stored only in the persistent E2B templates recorded by `material.toml` and
`receipts/e2b.json`.

This directory intentionally contains no checkout, direction, instruction, verifier,
solution, model credential, or rollout output. Do not force-build the fingerprint
Dockerfile; Harbor must reuse the recorded ready template alias.
"""


def render_baseline_script(repository: QualifiedRepository) -> str:
    command = command_with_environment(repository.test_cmd, repository.runtime_env)
    command = command_as_user(command, repository.execution_user)
    return f"#!/usr/bin/env bash\nset -euo pipefail\ncd /app\nexec {command}\n"


def render_export_patch_script(repository: QualifiedRepository) -> str:
    commit = shlex.quote(repository.base_commit)
    return (
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n"
        f"base_commit={commit}\n"
        "cd /app\n"
        "mkdir -p /logs/artifacts\n"
        'git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch\n'
    )


def build_e2b_receipt(
    repository: QualifiedRepository,
    *,
    environment_sha256: str,
    wrapper: E2BWrapperReceipt,
) -> dict[str, Any]:
    return {
        "schema_version": TRACE_MATERIAL_SCHEMA_VERSION,
        "validated_at": datetime.now(UTC).isoformat(),
        "harbor_cli_version": _package_version("harbor"),
        "e2b_sdk_version": _package_version("e2b"),
        "template_id": wrapper.harbor_template_id,
        "template_alias": wrapper.harbor_template_alias,
        "source_template_id": wrapper.source_template_id,
        "source_template_alias": repository.source_template_alias,
        "build_status": "ready",
        "execution_user": repository.execution_user,
        "resources": {
            "cpu_count": repository.cpu_count,
            "memory_mb": repository.memory_mb,
        },
        "wrapper_cache_hit": wrapper.cache_hit,
        "wrapper_build_duration_s": wrapper.build_duration_s,
        "environment_sha256": environment_sha256,
        "sandbox_smoke": wrapper.smoke,
        "sandbox_destroyed": bool(wrapper.smoke.get("sandbox_destroyed")),
    }


def render_catalog(packages: list[dict[str, Any]]) -> str:
    chunks = [f'schema_version = "{TRACE_MATERIAL_SCHEMA_VERSION}"\n']
    for package in sorted(packages, key=lambda item: str(item["material_id"])):
        chunks.append(
            "\n[[materials]]\n"
            f"id = {_toml_string(str(package['material_id']))}\n"
            'status = "qualified"\n'
            f"path = {_toml_string(str(package['material_path']))}\n"
            f"repository_url = {_toml_string(str(package['repository_url']))}\n"
            f"base_commit = {_toml_string(str(package['base_commit']))}\n"
            f"source_tree = {_toml_string(str(package['source_tree']))}\n"
            f"license = {_toml_string(str(package['license']))}\n"
            f"language = {_toml_string(str(package['language']))}\n"
        )
    return "".join(chunks)


def _package_version(package: str) -> str:
    try:
        return version(package)
    except PackageNotFoundError:
        return "unknown"


def _toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)
