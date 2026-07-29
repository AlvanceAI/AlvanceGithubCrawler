from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from .package_models import QualifiedRepository
from .runtime_profiles import command_as_user, command_with_environment

HARBOR_ENVELOPE_VERSION = "v2"


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
    except ImportError:
        digest = _directory_sha256(environment_dir)[:8]
    else:
        digest = dirhash(environment_dir, "sha256")[:8]
    return f"{task_name}__{digest}".replace(".", "-")


def _directory_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest()


def render_environment_dockerfile(repository: QualifiedRepository) -> str:
    return (
        f"# Harbor envelope {HARBOR_ENVELOPE_VERSION}\n"
        f"# Source E2B template: {repository.source_template_alias}\n"
        "# This file is an immutable Harbor fingerprint; do not force-build it.\n"
        "FROM e2bdev/base\n"
        "USER root\n"
        "WORKDIR /app\n"
    )


def render_instruction(repository: QualifiedRepository) -> str:
    fallback = "Inspect the repository and implement the requested change."
    return (
        "# Direction scaffold\n\n"
        "This file is a Crawler-produced direction scaffold, not a locked DeepSWE "
        "instruction and not an accepted task specification.\n\n"
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
        f"description = {_toml_string(f'E2B-backed repository task for {repository.repo}')}",
        "authors = []",
        f'keywords = [{_toml_string(repository.language)}, "e2b", "github"]',
        "",
        "[metadata]",
        f"task_id = {_toml_string(task)}",
        f"material_id = {_toml_string(material)}",
        'status = "direction"',
        f"language = {_toml_string(repository.language)}",
        f"repository_url = {_toml_string(repository.repository_url)}",
        f"base_commit_hash = {_toml_string(repository.base_commit)}",
        'storage_mode = "e2b-only"',
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
            "cpus = 2",
            "memory_mb = 4096",
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
    values = {
        "material_id": material,
        "catalog": "catalog/repo-materials.toml",
        "material_path": material_path,
        "repository_url": repository.repository_url,
        "base_commit": repository.base_commit,
        "source_tree": repository.source_tree,
        "environment_sha256": environment_sha256,
        "e2b_template_id": template_id,
        "e2b_template_alias": template_alias,
    }
    return "".join(f"{key} = {_toml_string(value)}\n" for key, value in values.items())


def _slug(value: str, *, limit: int) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:limit]


def _toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)
