from __future__ import annotations

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
from ..runtime.recipes import (
    SYSTEM_PACKAGES_COMMAND,
    repository_checkout_command,
    repository_dependency_commands,
    repository_finalize_commands,
    runtime_base_image,
    runtime_probe_command,
)
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
    dependency_commands: tuple[str, ...]
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
        runtime_template_id, runtime_cache_hit, runtime_build_s = self._ensure_runtime(
            Template,
            language,
            runtime_version,
            runtime_alias,
        )
        dependency_hash = hash_dependency_manifests(language, repo_path)
        dependency_commands = repository_dependency_commands(language, repo_path)
        repository_alias = repository_template_alias(
            str(repo["full_name"]),
            base_commit,
            dependency_hash,
            cpu_count=self.cpu_count,
            memory_mb=self.memory_mb,
        )
        (
            repository_template_id,
            repository_cache_hit,
            repository_build_s,
        ) = self._ensure_repository(
            Template,
            language,
            runtime_version,
            runtime_template_id,
            repository_alias,
            str(repo["full_name"]),
            base_commit,
            repo_path,
            str(repo.get("default_branch") or "main"),
            str(repo.get("source_tree") or ""),
            dependency_commands,
        )
        return E2BEnvironmentResult(
            runtime_version=runtime_version,
            runtime_template=runtime_template_id,
            repository_template=repository_template_id,
            runtime_alias=runtime_alias,
            repository_alias=repository_alias,
            dependency_hash=dependency_hash,
            runtime_cache_hit=runtime_cache_hit,
            repository_cache_hit=repository_cache_hit,
            runtime_template_build_s=round(runtime_build_s, 2),
            repository_template_build_s=round(repository_build_s, 2),
            test_cmd=test_command_for(language, repo_path),
            dependency_commands=dependency_commands,
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
    ) -> tuple[str, bool, float]:
        with self._alias_lock(runtime_alias):
            cache_hit = _template_alias_ready(Template, runtime_alias, self.api_key)
            if cache_hit:
                return runtime_alias, True, 0.0
            builder = _runtime_template_builder(Template, language, runtime_version)
            started = time.monotonic()
            logs = E2BBuildLogBuffer()
            try:
                info = Template.build(
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
            template_id = getattr(info, "template_id", None) or runtime_alias
            return template_id, False, time.monotonic() - started

    def _ensure_repository(
        self,
        Template: Any,
        language: str,
        runtime_version: str,
        runtime_template_id: str,
        repository_alias: str,
        full_name: str,
        base_commit: str,
        repo_path: Path,
        default_branch: str,
        source_tree: str,
        dependency_commands: tuple[str, ...],
    ) -> tuple[str, bool, float]:
        with self._alias_lock(repository_alias):
            cache_hit = _template_alias_ready(Template, repository_alias, self.api_key)
            if cache_hit:
                return repository_alias, True, 0.0
            builder = (
                Template()
                .from_template(runtime_template_id)
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
                source_tree=source_tree,
                dependency_commands=dependency_commands,
            )
            started = time.monotonic()
            logs = E2BBuildLogBuffer()
            try:
                info = Template.build(
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
            template_id = getattr(info, "template_id", None) or repository_alias
            return template_id, False, time.monotonic() - started

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
    source_tree: str = "",
    dependency_commands: tuple[str, ...] | None = None,
) -> Any:
    builder = builder.run_cmd(
        repository_checkout_command(
            full_name,
            base_commit,
            default_branch,
            source_tree=source_tree,
        ),
        user="root",
    ).set_workdir("/app")
    commands = dependency_commands or repository_dependency_commands(language, repo_path)
    for command in (*commands, *repository_finalize_commands(language)):
        builder = builder.run_cmd(command, user="root")
    return builder


def _runtime_template_builder(Template: Any, language: str, version: str) -> Any:
    return (
        Template()
        .from_image(runtime_base_image(language, version))
        .set_envs(runtime_environment(language, version))
        .run_cmd(SYSTEM_PACKAGES_COMMAND, user="root")
        .run_cmd(runtime_probe_command(language), user="root")
        .set_workdir("/app")
    )
