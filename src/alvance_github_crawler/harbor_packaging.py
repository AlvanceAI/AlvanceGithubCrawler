from __future__ import annotations

import base64
import hashlib
import json
import re
import shlex
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import requests

from .e2b_environment import command_with_environment, runtime_environment

HARBOR_PACKAGE_SCHEMA_VERSION = "1.0"
HARBOR_ENVELOPE_VERSION = "v1"


@dataclass(slots=True)
class HarborPackageResult:
    package_id: str
    task_name: str
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


class HarborPackager:
    """Create tiny Harbor task envelopes backed only by persistent E2B templates."""

    def __init__(
        self,
        api_key: str,
        catalog_dir: Path,
        *,
        cpu_count: int = 2,
        memory_mb: int = 4_096,
    ) -> None:
        self.api_key = api_key
        self.catalog_dir = catalog_dir
        self.cpu_count = cpu_count
        self.memory_mb = memory_mb

    def package(self, record: dict[str, Any]) -> HarborPackageResult:
        environment = record.get("e2b_environment") or {}
        source_alias = str(record.get("e2b_template") or "")
        if not source_alias:
            raise ValueError("candidate has no E2B repository template")

        repo = str(record["repo"])
        base_commit = str(record["base_commit"])
        language = str(record["language"]).lower()
        runtime_version = str(environment["runtime_version"])
        test_cmd = str(record["test_cmd"])
        envs = runtime_environment(language, runtime_version)
        task_name = harbor_task_name(repo, base_commit)
        task_dir = self.catalog_dir / "harbor" / task_name
        write_task_envelope(
            task_dir,
            task_name=task_name,
            repo=repo,
            base_commit=base_commit,
            language=language,
            direction=str(record.get("direction") or ""),
            source_template_alias=source_alias,
            test_cmd=test_cmd,
            envs=envs,
        )
        harbor_alias = harbor_template_alias(task_dir)

        wrapper_cache_hit, wrapper_id, wrapper_build_s = self._ensure_wrapper(
            source_alias,
            harbor_alias,
            language,
            envs,
        )
        source_id = self._resolve_template_id(source_alias)
        smoke_ok = self._smoke(harbor_alias, language)
        if not smoke_ok:
            raise RuntimeError(f"Harbor E2B wrapper smoke failed: {harbor_alias}")

        result = HarborPackageResult(
            package_id=task_name,
            task_name=task_name,
            task_path=task_dir.as_posix(),
            source_template_alias=source_alias,
            source_template_id=source_id,
            harbor_template_alias=harbor_alias,
            harbor_template_id=wrapper_id,
            wrapper_cache_hit=wrapper_cache_hit,
            wrapper_build_s=round(wrapper_build_s, 2),
            smoke_ok=smoke_ok,
            launch_command=(
                f"harbor run --path {shlex.quote(task_dir.as_posix())} "
                "--env e2b --no-force-build"
            ),
        )
        package_record = compact_package_record(record, result, envs)
        (task_dir / "e2b.json").write_text(
            json.dumps(package_record, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )
        self._upsert_catalog(package_record)
        return result

    def package_existing(self, candidates_path: Path) -> dict[str, int]:
        stats = {"processed": 0, "packaged": 0, "error": 0}
        if not candidates_path.is_file():
            return stats
        for line in candidates_path.read_text(encoding="utf-8").splitlines():
            try:
                record = json.loads(line)
                stats["processed"] += 1
                self.package(record)
                stats["packaged"] += 1
            except Exception:
                stats["error"] += 1
        return stats

    def _ensure_wrapper(
        self,
        source_alias: str,
        harbor_alias: str,
        language: str,
        envs: dict[str, str],
    ) -> tuple[bool, str, float]:
        try:
            from e2b import Template
        except ImportError as exc:
            raise RuntimeError("e2b SDK is required for Harbor packaging") from exc

        cache_hit = Template.alias_exists(harbor_alias, api_key=self.api_key)
        build_s = 0.0
        if not cache_hit:
            builder = Template().from_template(source_alias).set_workdir("/repo")
            builder = add_harbor_runtime_wrappers(builder, language, envs)
            started = time.monotonic()
            info = Template.build(
                builder,
                name=harbor_alias,
                cpu_count=self.cpu_count,
                memory_mb=self.memory_mb,
                skip_cache=False,
                api_key=self.api_key,
            )
            build_s = time.monotonic() - started
            return cache_hit, info.template_id, build_s
        return cache_hit, self._resolve_template_id(harbor_alias), build_s

    def _resolve_template_id(self, alias: str) -> str:
        response = requests.get(
            f"https://api.e2b.app/templates/aliases/{alias}",
            headers={"X-API-Key": self.api_key},
            timeout=30,
        )
        response.raise_for_status()
        return str(response.json()["templateID"])

    def _smoke(self, harbor_alias: str, language: str) -> bool:
        try:
            from e2b import Sandbox
        except ImportError as exc:
            raise RuntimeError("e2b SDK is required for Harbor packaging") from exc

        probe = runtime_probe(language)
        with Sandbox.create(
            template=harbor_alias,
            allow_internet_access=False,
            timeout=120,
            api_key=self.api_key,
        ) as sandbox:
            result = sandbox.commands.run(
                f"cd /repo && test -d . && {probe}",
                user="root",
                timeout=60,
            )
        return result.exit_code == 0

    def _upsert_catalog(self, package: dict[str, Any]) -> None:
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
                if package_id:
                    packages[package_id] = existing
        packages[str(package["package_id"])] = package
        payload = "".join(
            json.dumps(packages[key], ensure_ascii=False, sort_keys=True) + "\n"
            for key in sorted(packages)
        )
        path.write_text(payload, encoding="utf-8")


def harbor_task_name(repo: str, base_commit: str) -> str:
    repo_name = repo.rsplit("/", 1)[-1].lower()
    repo_slug = re.sub(r"[^a-z0-9]+", "-", repo_name).strip("-")[:20]
    owner_hash = hashlib.sha256(repo.encode()).hexdigest()[:6]
    return f"alv-{repo_slug}-{owner_hash}-{base_commit[:8]}-{HARBOR_ENVELOPE_VERSION}"


def harbor_template_alias(task_dir: Path) -> str:
    try:
        from dirhash import dirhash
    except ImportError as exc:
        raise RuntimeError("dirhash is required for Harbor packaging") from exc
    digest = dirhash(task_dir / "environment", "sha256")[:8]
    return f"{task_dir.name}__{digest}".replace(".", "-")


def write_task_envelope(
    task_dir: Path,
    *,
    task_name: str,
    repo: str,
    base_commit: str,
    language: str,
    direction: str,
    source_template_alias: str,
    test_cmd: str,
    envs: dict[str, str],
) -> None:
    environment_dir = task_dir / "environment"
    tests_dir = task_dir / "tests"
    solution_dir = task_dir / "solution"
    environment_dir.mkdir(parents=True, exist_ok=True)
    tests_dir.mkdir(parents=True, exist_ok=True)
    solution_dir.mkdir(parents=True, exist_ok=True)

    dockerfile = (
        f"# Harbor envelope {HARBOR_ENVELOPE_VERSION}\n"
        f"# Source E2B template: {source_template_alias}\n"
        "FROM e2bdev/base\n"
        "USER root\n"
        "WORKDIR /repo\n"
    )
    (environment_dir / "Dockerfile").write_text(dockerfile, encoding="utf-8")

    fallback_direction = "Inspect the repository and implement the requested change."
    instruction = (
        f"Repository `{repo}` at commit `{base_commit}` is preloaded in `/repo`.\n\n"
        "Work in `/repo`. The validated direction is:\n\n"
        f"{direction or fallback_direction}\n"
    )
    (task_dir / "instruction.md").write_text(instruction, encoding="utf-8")

    task_toml = render_task_toml(
        task_name=task_name,
        repo=repo,
        base_commit=base_commit,
        language=language,
        envs=envs,
    )
    (task_dir / "task.toml").write_text(task_toml, encoding="utf-8")

    test_script = (
        "#!/bin/sh\n"
        "set -eu\n"
        "cd /repo\n"
        f"exec {command_with_environment(test_cmd, envs)}\n"
    )
    test_path = tests_dir / "test.sh"
    test_path.write_text(test_script, encoding="utf-8")
    test_path.chmod(0o755)

    solve_path = solution_dir / "solve.sh"
    solve_path.write_text("#!/bin/sh\nset -eu\nexit 0\n", encoding="utf-8")
    solve_path.chmod(0o755)


def render_task_toml(
    *,
    task_name: str,
    repo: str,
    base_commit: str,
    language: str,
    envs: dict[str, str],
) -> str:
    lines = [
        'version = "1.0"',
        'schema_version = "1.3"',
        "",
        "[task]",
        f"name = {json.dumps(f'alvance/{task_name}')}",
        f"description = {json.dumps(f'E2B-backed repository task for {repo}')}",
        "authors = []",
        f"keywords = [{json.dumps(language)}, \"e2b\", \"github\"]",
        "",
        "[metadata]",
        f"repository_url = {json.dumps(f'https://github.com/{repo}')}",
        f"base_commit_hash = {json.dumps(base_commit)}",
        f"language = {json.dumps(language)}",
        'storage_mode = "e2b-only"',
        "",
        "[verifier]",
        "timeout_sec = 600.0",
        'environment_mode = "shared"',
        "",
        "[verifier.env]",
    ]
    lines.extend(f"{key} = {json.dumps(value)}" for key, value in sorted(envs.items()))
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


def add_harbor_runtime_wrappers(
    builder: Any,
    language: str,
    envs: dict[str, str],
) -> Any:
    language = language.lower()
    targets: dict[str, str] = {}
    if language == "go":
        targets = {
            "go": "/usr/local/go/bin/go",
            "gofmt": "/usr/local/go/bin/gofmt",
        }
    elif language == "rust":
        targets = {
            "cargo": "/usr/local/cargo/bin/cargo",
            "rustc": "/usr/local/cargo/bin/rustc",
            "rustup": "/usr/local/cargo/bin/rustup",
        }

    for name, target in targets.items():
        script = "#!/bin/sh\n" + "".join(
            f"export {key}={shlex.quote(value)}\n" for key, value in sorted(envs.items())
        )
        script += f'exec {target} "$@"\n'
        encoded = base64.b64encode(script.encode()).decode()
        builder = builder.run_cmd(
            f"printf %s {shlex.quote(encoded)} | base64 -d > /usr/local/bin/{name} "
            f"&& chmod 0755 /usr/local/bin/{name}",
            user="root",
        )
    return builder


def runtime_probe(language: str) -> str:
    language = language.lower()
    if language == "go":
        return "go version"
    if language == "python":
        return "python --version"
    if language in {"typescript", "javascript"}:
        return "node --version"
    if language == "rust":
        return "cargo --version"
    raise ValueError(f"unsupported language: {language}")


def compact_package_record(
    record: dict[str, Any],
    result: HarborPackageResult,
    envs: dict[str, str],
) -> dict[str, Any]:
    environment = record.get("e2b_environment") or {}
    offline = environment.get("offline") or {}
    benchmark = record.get("benchmark") or {}
    return {
        "schema_version": HARBOR_PACKAGE_SCHEMA_VERSION,
        "package_id": result.package_id,
        "repo": record["repo"],
        "repository_url": f"https://github.com/{record['repo']}",
        "base_commit": record["base_commit"],
        "language": record["language"],
        "workdir": "/repo",
        "test_cmd": record["test_cmd"],
        "runtime_version": environment.get("runtime_version"),
        "runtime_env": envs,
        "source_template": {
            "alias": result.source_template_alias,
            "template_id": result.source_template_id,
        },
        "harbor": {
            "task_name": result.task_name,
            "task_path": result.task_path,
            "template_alias": result.harbor_template_alias,
            "template_id": result.harbor_template_id,
            "launch_command": result.launch_command,
            "smoke_ok": result.smoke_ok,
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
            "remote_e2b_only": True,
        },
    }
