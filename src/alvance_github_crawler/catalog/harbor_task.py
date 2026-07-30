from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from ..runtime.profiles import command_as_user, command_with_environment
from ..runtime.recipes import (
    SYSTEM_PACKAGES_COMMAND,
    repository_checkout_command,
    repository_finalize_commands,
    runtime_base_image,
    runtime_probe_command,
)
from .package_models import QualifiedRepository

HARBOR_ENVELOPE_VERSION = "v2"
DOCKERFILE_RECIPE_VERSION = "v3"


def material_id(repository: QualifiedRepository) -> str:
    repo_name = _slug(repository.repo.rsplit("/", 1)[-1], limit=24)
    owner_hash = hashlib.sha256(repository.repo.encode()).hexdigest()[:6]
    return f"{repo_name}-{owner_hash}-{repository.base_commit[:8]}"


def task_name(repository: QualifiedRepository) -> str:
    repo_name = _slug(repository.repo.rsplit("/", 1)[-1], limit=20)
    owner_hash = hashlib.sha256(repository.repo.encode()).hexdigest()[:6]
    return f"alv-{repo_name}-{owner_hash}-{repository.base_commit[:8]}-{HARBOR_ENVELOPE_VERSION}"


def harbor_template_alias(task_name: str, environment_dir: Path) -> str:
    try:
        from dirhash import dirhash
    except ImportError as exc:
        raise RuntimeError("dirhash is required for Harbor packaging") from exc
    digest = dirhash(environment_dir, "sha256")[:8]
    return f"{task_name}-env-{digest}".replace(".", "-")


def render_environment_dockerfile(repository: QualifiedRepository) -> str:
    lines = [
        f"# Harbor rebuildable envelope {HARBOR_ENVELOPE_VERSION}",
        f"# Dockerfile recipe {DOCKERFILE_RECIPE_VERSION}",
        "# E2B aliases are optional caches; this file is the durable build source.",
        f"FROM {runtime_base_image(repository.language, repository.runtime_version)}",
        "USER root",
    ]
    lines.extend(
        f"ENV {key}={json.dumps(value)}" for key, value in sorted(repository.runtime_env.items())
    )
    lines.extend(
        [
            f"RUN {SYSTEM_PACKAGES_COMMAND}",
            f"RUN {runtime_probe_command(repository.language)}",
        ]
    )
    if repository.execution_user == "user":
        lines.append(
            "RUN id -u user >/dev/null 2>&1 "
            "|| useradd --create-home --shell /bin/bash user"
        )
    lines.extend(
        [
            "WORKDIR /",
            "RUN "
            + repository_checkout_command(
                repository.repo,
                repository.base_commit,
                repository.default_branch,
                source_tree=repository.source_tree,
            ),
            "WORKDIR /app",
        ]
    )
    lines.extend(f"RUN {command}" for command in repository.dependency_commands)
    lines.extend(
        f"RUN {command}" for command in repository_finalize_commands(repository.language)
    )
    lines.extend(["USER root", "WORKDIR /app", ""])
    return "\n".join(lines)


def render_instruction(repository: QualifiedRepository) -> str:
    fallback = "Inspect the repository and implement the requested change."
    return (
        f"Repository `{repository.repo}` at commit `{repository.base_commit}` is "
        "preloaded in `/app`.\n\n"
        "Work in `/app`. The validated fuzzy direction is:\n\n"
        f"{repository.direction or fallback}\n"
    )


def render_task_toml(repository: QualifiedRepository, task: str, material: str) -> str:
    lines = [
        'version = "1.0"',
        'schema_version = "1.3"',
        "",
        "[task]",
        f"name = {_toml_string(f'alvance/{task}')}",
        f"description = {_toml_string(f'Rebuildable repository task for {repository.repo}')}",
        "authors = []",
        f'keywords = [{_toml_string(repository.language)}, "dockerfile", "github"]',
        "",
        "[metadata]",
        f"task_id = {_toml_string(task)}",
        f"material_id = {_toml_string(material)}",
        'status = "direction"',
        f"language = {_toml_string(repository.language)}",
        f"repository_url = {_toml_string(repository.repository_url)}",
        f"base_commit_hash = {_toml_string(repository.base_commit)}",
        'storage_mode = "dockerfile-rebuildable"',
        "dockerfile_rebuildable = true",
        "rebuild_network_required = true",
        "",
        "[verifier]",
        "timeout_sec = 600.0",
        'environment_mode = "shared"',
        "",
        "[verifier.env]",
    ]
    lines.extend(
        f"{key} = {_toml_string(value)}" for key, value in sorted(repository.runtime_env.items())
    )
    lines.extend(
        [
            "",
            "[agent]",
            "timeout_sec = 5400.0",
            "",
            "[environment]",
            "build_timeout_sec = 3600.0",
            f"cpus = {repository.cpu_count}",
            f"memory_mb = {repository.memory_mb}",
            "storage_mb = 10240",
            "gpus = 0",
            "allow_internet = true",
            "mcp_servers = []",
            "",
        ]
    )
    return "\n".join(lines)


def render_test_script(repository: QualifiedRepository) -> str:
    command = command_with_environment(repository.test_cmd, repository.runtime_env)
    command = command_as_user(command, repository.execution_user)
    return (
        "#!/bin/sh\n"
        "set -u\n"
        "mkdir -p /logs/verifier\n"
        "cd /app\n"
        f"if {command}; then\n"
        "    echo 1 > /logs/verifier/reward.txt\n"
        "    exit 0\n"
        "else\n"
        "    status=$?\n"
        "    echo 0 > /logs/verifier/reward.txt\n"
        '    exit "$status"\n'
        "fi\n"
    )


def render_task_material_toml(
    repository: QualifiedRepository,
    *,
    material: str,
    material_path: str,
    environment_sha256: str,
    template_id: str,
    template_alias: str,
) -> str:
    values: dict[str, object] = {
        "schema_version": "0.3",
        "material_id": material,
        "catalog": "catalog/repo-materials.toml",
        "material_path": material_path,
        "repository_url": repository.repository_url,
        "base_commit": repository.base_commit,
        "source_tree": repository.source_tree,
        "environment_sha256": environment_sha256,
        "dockerfile_rebuildable": True,
        "rebuild_network_required": True,
    }
    lines = [f"{key} = {_toml_value(value)}" for key, value in values.items()]
    lines.extend(
        [
            "",
            "[e2b_history]",
            f"template_id = {_toml_string(template_id)}",
            f"template_alias = {_toml_string(template_alias)}",
            "operational_dependency = false",
            "",
        ]
    )
    return "\n".join(lines)


def _slug(value: str, *, limit: int) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:limit]


def _toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _toml_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return _toml_string(str(value))
