from __future__ import annotations

import shlex
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .build import test_command_for
from .runtime_profiles import (
    detect_runtime_version,
    hash_dependency_manifests,
    repository_template_alias,
    runtime_environment,
    runtime_template_alias,
)


class RuntimeTemplateBuildError(RuntimeError):
    pass


class RepositoryTemplateBuildError(RuntimeError):
    pass


@dataclass(slots=True)
class E2BEnvironmentResult:
    runtime_version: str
    runtime_template: str
    repository_template: str
    runtime_alias: str
    repository_alias: str
    dependency_hash: str
    runtime_cache_hit: bool
    repository_cache_hit: bool
    runtime_template_build_s: float
    repository_template_build_s: float
    test_cmd: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class E2BEnvironmentManager:
    def __init__(
        self,
        api_key: str,
        *,
        cpu_count: int = 2,
        memory_mb: int = 4_096,
    ) -> None:
        self.api_key = api_key
        self.cpu_count = cpu_count
        self.memory_mb = memory_mb

    def ensure(
        self,
        repo: dict[str, Any],
        repo_path: Path,
        base_commit: str,
    ) -> E2BEnvironmentResult:
        try:
            from e2b import Template
        except ImportError as exc:
            raise RuntimeTemplateBuildError(
                "e2b SDK is not installed; install the project with [e2b]"
            ) from exc

        language = str(repo.get("language") or "").lower()
        runtime_version = detect_runtime_version(language, repo_path)
        runtime_alias = runtime_template_alias(language, runtime_version)
        runtime_cache_hit, runtime_build_s = self._ensure_runtime(
            Template,
            language,
            runtime_version,
            runtime_alias,
        )
        dependency_hash = hash_dependency_manifests(language, repo_path)
        repository_alias = repository_template_alias(
            str(repo["full_name"]),
            base_commit,
            dependency_hash,
        )
        repository_cache_hit, repository_build_s = self._ensure_repository(
            Template,
            language,
            runtime_version,
            runtime_alias,
            repository_alias,
            str(repo["full_name"]),
            base_commit,
        )
        return E2BEnvironmentResult(
            runtime_version=runtime_version,
            runtime_template=runtime_alias,
            repository_template=repository_alias,
            runtime_alias=runtime_alias,
            repository_alias=repository_alias,
            dependency_hash=dependency_hash,
            runtime_cache_hit=runtime_cache_hit,
            repository_cache_hit=repository_cache_hit,
            runtime_template_build_s=round(runtime_build_s, 2),
            repository_template_build_s=round(repository_build_s, 2),
            test_cmd=test_command_for(language, repo_path),
        )

    def _ensure_runtime(
        self,
        Template: Any,
        language: str,
        runtime_version: str,
        runtime_alias: str,
    ) -> tuple[bool, float]:
        cache_hit = Template.alias_exists(runtime_alias, api_key=self.api_key)
        if cache_hit:
            return True, 0.0
        builder = _runtime_template_builder(Template, language, runtime_version)
        started = time.monotonic()
        try:
            Template.build(
                builder,
                name=runtime_alias,
                cpu_count=self.cpu_count,
                memory_mb=self.memory_mb,
                skip_cache=False,
                api_key=self.api_key,
            )
        except Exception as exc:
            raise RuntimeTemplateBuildError(str(exc)) from exc
        return False, time.monotonic() - started

    def _ensure_repository(
        self,
        Template: Any,
        language: str,
        runtime_version: str,
        runtime_alias: str,
        repository_alias: str,
        full_name: str,
        base_commit: str,
    ) -> tuple[bool, float]:
        cache_hit = Template.alias_exists(repository_alias, api_key=self.api_key)
        if cache_hit:
            return True, 0.0
        builder = (
            Template()
            .from_template(runtime_alias)
            .set_envs(runtime_environment(language, runtime_version))
            .set_workdir("/")
        )
        builder = _add_repository_build_steps(
            builder,
            language,
            full_name,
            base_commit,
        )
        started = time.monotonic()
        try:
            Template.build(
                builder,
                name=repository_alias,
                cpu_count=self.cpu_count,
                memory_mb=self.memory_mb,
                skip_cache=False,
                api_key=self.api_key,
            )
        except Exception as exc:
            raise RepositoryTemplateBuildError(str(exc)) from exc
        return False, time.monotonic() - started


def _add_repository_build_steps(
    builder: Any,
    language: str,
    full_name: str,
    base_commit: str,
) -> Any:
    repository_url = shlex.quote(f"https://github.com/{full_name}.git")
    commit = shlex.quote(base_commit)
    builder = builder.run_cmd(
        "rm -rf /app && mkdir -p /app && git init /app && cd /app "
        f"&& git remote add origin {repository_url} "
        f"&& git fetch --depth=1 origin {commit} "
        "&& git checkout --detach FETCH_HEAD "
        "&& git submodule update --init --recursive "
        "&& git remote remove origin",
        user="root",
    ).set_workdir("/app")
    if language == "go":
        builder = builder.run_cmd("/usr/local/go/bin/go mod download", user="root")
        builder = builder.run_cmd("/usr/local/go/bin/go build ./...", user="root")
    elif language in {"typescript", "javascript"}:
        builder = builder.run_cmd("/usr/local/bin/npm ci", user="root")
    elif language == "python":
        builder = builder.run_cmd(
            "/usr/local/bin/pip install --no-cache-dir -e '.[test,dev]' || "
            "/usr/local/bin/pip install --no-cache-dir -e .",
            user="root",
        )
    elif language == "rust":
        builder = builder.run_cmd(
            "/usr/local/cargo/bin/cargo build --tests",
            user="root",
        )
    else:
        raise ValueError(f"unsupported language: {language}")
    return builder.run_cmd('test -z "$(git status --porcelain)"', user="root")


def _runtime_template_builder(Template: Any, language: str, version: str) -> Any:
    packages = (
        "apt-get update && apt-get install -y --no-install-recommends "
        "time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*"
    )
    image, probe = {
        "go": ("docker.io/library/golang:1.22", "/usr/local/go/bin/go version"),
        "python": (
            f"docker.io/library/python:{version}",
            "/usr/local/bin/python --version && /usr/local/bin/pip --version",
        ),
        "typescript": (
            f"docker.io/library/node:{version}",
            "/usr/local/bin/node --version && /usr/local/bin/npm --version",
        ),
        "javascript": (
            f"docker.io/library/node:{version}",
            "/usr/local/bin/node --version && /usr/local/bin/npm --version",
        ),
        "rust": (
            f"docker.io/library/rust:{version}",
            "/usr/local/cargo/bin/rustc --version && /usr/local/cargo/bin/cargo --version",
        ),
    }[language]
    return (
        Template()
        .from_image(image)
        .set_envs(runtime_environment(language, version))
        .run_cmd(packages, user="root")
        .run_cmd(probe, user="root")
        .set_workdir("/app")
    )
