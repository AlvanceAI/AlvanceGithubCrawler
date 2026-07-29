from __future__ import annotations

import shlex
import threading
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from ..runtime.build import test_command_for
from ..runtime.profiles import (
    detect_runtime_version,
    execution_user,
    hash_dependency_manifests,
    repository_template_alias,
    runtime_environment,
    runtime_template_alias,
)
from ..runtime.python import python_install_commands
from .build_logs import E2BBuildLogBuffer


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
    execution_user: str
    cpu_count: int
    memory_mb: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class E2BEnvironmentManager:
    def __init__(
        self,
        api_key: str,
        *,
        cpu_count: int = 1,
        memory_mb: int = 1_024,
    ) -> None:
        self.api_key = api_key
        self.cpu_count = cpu_count
        self.memory_mb = memory_mb
        self._alias_locks: dict[str, threading.Lock] = {}
        self._alias_locks_guard = threading.Lock()

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
        runtime_alias = runtime_template_alias(
            language,
            runtime_version,
            cpu_count=self.cpu_count,
            memory_mb=self.memory_mb,
        )
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
            cpu_count=self.cpu_count,
            memory_mb=self.memory_mb,
        )
        repository_cache_hit, repository_build_s = self._ensure_repository(
            Template,
            language,
            runtime_version,
            runtime_alias,
            repository_alias,
            str(repo["full_name"]),
            base_commit,
            repo_path,
            str(repo.get("default_branch") or "main"),
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
            execution_user=execution_user(language),
            cpu_count=self.cpu_count,
            memory_mb=self.memory_mb,
        )

    def _ensure_runtime(
        self,
        Template: Any,
        language: str,
        runtime_version: str,
        runtime_alias: str,
    ) -> tuple[bool, float]:
        with self._alias_lock(runtime_alias):
            cache_hit = _template_alias_ready(Template, runtime_alias, self.api_key)
            if cache_hit:
                return True, 0.0
            builder = _runtime_template_builder(Template, language, runtime_version)
            started = time.monotonic()
            logs = E2BBuildLogBuffer()
            try:
                Template.build(
                    builder,
                    name=runtime_alias,
                    cpu_count=self.cpu_count,
                    memory_mb=self.memory_mb,
                    skip_cache=False,
                    api_key=self.api_key,
                    on_build_logs=logs,
                )
            except Exception as exc:
                raise RuntimeTemplateBuildError(logs.error_message(exc)) from exc
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
        repo_path: Path,
        default_branch: str,
    ) -> tuple[bool, float]:
        with self._alias_lock(repository_alias):
            cache_hit = _template_alias_ready(Template, repository_alias, self.api_key)
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
                repo_path=repo_path,
                default_branch=default_branch,
            )
            started = time.monotonic()
            logs = E2BBuildLogBuffer()
            try:
                Template.build(
                    builder,
                    name=repository_alias,
                    cpu_count=self.cpu_count,
                    memory_mb=self.memory_mb,
                    skip_cache=False,
                    api_key=self.api_key,
                    on_build_logs=logs,
                )
            except Exception as exc:
                raise RepositoryTemplateBuildError(logs.error_message(exc)) from exc
            return False, time.monotonic() - started

    def _alias_lock(self, alias: str) -> threading.Lock:
        with self._alias_locks_guard:
            return self._alias_locks.setdefault(alias, threading.Lock())


def _template_alias_ready(Template: Any, alias: str, api_key: str) -> bool:
    # Failed E2B builds can leave an unlaunchable bare alias without a usable tag.
    return bool(Template.alias_exists(f"{alias}:default", api_key=api_key))


def _add_repository_build_steps(
    builder: Any,
    language: str,
    full_name: str,
    base_commit: str,
    *,
    repo_path: Path | None = None,
    default_branch: str = "main",
) -> Any:
    repository_url = shlex.quote(f"https://github.com/{full_name}.git")
    commit = shlex.quote(base_commit)
    branch = shlex.quote(default_branch)
    builder = builder.run_cmd(
        "rm -rf /app && mkdir -p /app && git init /app && cd /app "
        f"&& git remote add origin {repository_url} "
        f"&& git fetch --depth=1 origin {commit} "
        "&& git checkout --detach FETCH_HEAD "
        "&& git submodule update --init --recursive "
        f"&& git update-ref refs/remotes/origin/{branch} HEAD",
        user="root",
    ).set_workdir("/app")
    if language == "go":
        builder = builder.run_cmd("/usr/local/go/bin/go mod download", user="root")
        builder = builder.run_cmd("/usr/local/go/bin/go build ./...", user="root")
    elif language in {"typescript", "javascript"}:
        builder = builder.run_cmd("/usr/local/bin/npm ci", user="root")
    elif language == "python":
        if repo_path is None:
            raise ValueError("repo_path is required for Python repository templates")
        for command in python_install_commands(repo_path):
            builder = builder.run_cmd(command, user="root")
    elif language == "rust":
        builder = builder.run_cmd(
            "/usr/local/cargo/bin/cargo build --tests",
            user="root",
        )
    else:
        raise ValueError(f"unsupported language: {language}")
    builder = builder.run_cmd('test -z "$(git status --porcelain)"', user="root")
    if language == "python":
        builder = builder.run_cmd("chown -R user:user /app", user="root")
    return builder


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
