from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .build import test_command_for

RUNTIME_RECIPE_VERSION = "v1"
REPOSITORY_RECIPE_VERSION = "v1"

DEFAULT_RUNTIME_VERSIONS = {
    "go": "1.22",
    "python": "3.11",
    "typescript": "20",
    "javascript": "20",
    "rust": "1.77",
}

DEPENDENCY_FILES = {
    "go": ("go.mod", "go.sum"),
    "python": (
        "pyproject.toml",
        "poetry.lock",
        "uv.lock",
        "requirements.txt",
        "requirements-dev.txt",
        "requirements-test.txt",
    ),
    "typescript": (
        "package.json",
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
    ),
    "javascript": (
        "package.json",
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
    ),
    "rust": ("Cargo.toml", "Cargo.lock"),
}


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


@dataclass(slots=True)
class OfflineTestResult:
    ok: bool
    reason: str
    duration_s: float
    exit_code: int
    stdout_tail: str = ""
    stderr_tail: str = ""

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

        language = (repo.get("language") or "").lower()
        runtime_version = detect_runtime_version(language, repo_path)
        runtime_alias = runtime_template_alias(language, runtime_version)
        runtime_cache_hit = Template.alias_exists(runtime_alias, api_key=self.api_key)
        runtime_build_s = 0.0
        if not runtime_cache_hit:
            started = time.monotonic()
            runtime_builder = Template().from_dockerfile(
                render_runtime_dockerfile(language, runtime_version)
            )
            try:
                Template.build(
                    runtime_builder,
                    name=runtime_alias,
                    alias=runtime_alias,
                    cpu_count=self.cpu_count,
                    memory_mb=self.memory_mb,
                    skip_cache=False,
                    api_key=self.api_key,
                )
            except Exception as exc:
                raise RuntimeTemplateBuildError(str(exc)) from exc
            runtime_build_s = time.monotonic() - started

        dependency_hash = hash_dependency_manifests(language, repo_path)
        repository_alias = repository_template_alias(
            repo["full_name"], base_commit, dependency_hash
        )
        repository_cache_hit = Template.alias_exists(
            repository_alias, api_key=self.api_key
        )
        repository_build_s = 0.0
        if not repository_cache_hit:
            builder = Template(file_context_path=repo_path).from_template(runtime_alias)
            builder = builder.set_workdir("/repo")
            builder = _add_repository_build_steps(builder, language, repo_path)
            started = time.monotonic()
            try:
                Template.build(
                    builder,
                    name=repository_alias,
                    alias=repository_alias,
                    cpu_count=self.cpu_count,
                    memory_mb=self.memory_mb,
                    skip_cache=False,
                    api_key=self.api_key,
                )
            except Exception as exc:
                raise RepositoryTemplateBuildError(str(exc)) from exc
            repository_build_s = time.monotonic() - started

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


class E2BOfflineVerifier:
    def __init__(self, api_key: str, *, timeout_s: int = 600) -> None:
        self.api_key = api_key
        self.timeout_s = timeout_s

    def verify(self, template: str, test_cmd: str) -> OfflineTestResult:
        try:
            from e2b import Sandbox
        except ImportError as exc:
            raise RuntimeError("e2b SDK is not installed; install the project with [e2b]") from exc

        started = time.monotonic()
        with Sandbox.create(
            template=template,
            allow_internet_access=False,
            timeout=self.timeout_s + 60,
            api_key=self.api_key,
        ) as sandbox:
            result = sandbox.commands.run(test_cmd, timeout=self.timeout_s)
        duration = time.monotonic() - started
        return OfflineTestResult(
            ok=result.exit_code == 0,
            reason="ok" if result.exit_code == 0 else "offline_test_fail",
            duration_s=round(duration, 2),
            exit_code=result.exit_code,
            stdout_tail=(result.stdout or "")[-4_000:],
            stderr_tail=(result.stderr or "")[-4_000:],
        )


def detect_runtime_version(language: str, repo_path: Path) -> str:
    language = language.lower()
    if language == "go":
        match = re.search(
            r"^go\s+(\d+\.\d+(?:\.\d+)?)\s*$",
            _read(repo_path / "go.mod"),
            re.MULTILINE,
        )
        return match.group(1) if match else DEFAULT_RUNTIME_VERSIONS[language]
    if language == "python":
        match = re.search(
            r"requires-python\s*=\s*['\"][^'\"]*?(\d+\.\d+)",
            _read(repo_path / "pyproject.toml"),
        )
        return match.group(1) if match else DEFAULT_RUNTIME_VERSIONS[language]
    if language in {"typescript", "javascript"}:
        try:
            package = json.loads(_read(repo_path / "package.json") or "{}")
        except json.JSONDecodeError:
            package = {}
        engine = str((package.get("engines") or {}).get("node", ""))
        majors = [int(value) for value in re.findall(r"(?<!\d)(\d{2})(?:\.\d+)?", engine)]
        return str(max(20, min(majors))) if majors else DEFAULT_RUNTIME_VERSIONS[language]
    if language == "rust":
        content = _read(repo_path / "rust-toolchain.toml") or _read(
            repo_path / "rust-toolchain"
        )
        match = re.search(r"(?:channel\s*=\s*)?['\"]?(\d+\.\d+(?:\.\d+)?)", content)
        return match.group(1) if match else DEFAULT_RUNTIME_VERSIONS[language]
    raise ValueError(f"unsupported language: {language}")


def render_runtime_dockerfile(language: str, version: str) -> str:
    apt = (
        "RUN apt-get update && apt-get install -y --no-install-recommends "
        "time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*"
    )
    language = language.lower()
    if language == "go":
        return f"""FROM golang:1.22
ENV PATH=/usr/local/go/bin:/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV GOPROXY=https://goproxy.cn,direct
ENV GOTOOLCHAIN=go{version}+auto
{apt}
RUN go version
WORKDIR /repo
"""
    if language == "python":
        return f"""FROM python:{version}
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin
{apt}
RUN python --version && pip --version
WORKDIR /repo
"""
    if language in {"typescript", "javascript"}:
        return f"""FROM node:{version}
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin
{apt}
RUN node --version && npm --version
WORKDIR /repo
"""
    if language == "rust":
        return f"""FROM rust:{version}
ENV PATH=/usr/local/cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
{apt}
RUN rustc --version && cargo --version
WORKDIR /repo
"""
    raise ValueError(f"unsupported language: {language}")


def hash_dependency_manifests(language: str, repo_path: Path) -> str:
    digest = hashlib.sha256()
    found = False
    for name in DEPENDENCY_FILES.get(language.lower(), ()):
        path = repo_path / name
        if not path.is_file():
            continue
        found = True
        digest.update(name.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    if not found:
        digest.update(b"no-dependency-manifest")
    return digest.hexdigest()[:16]


def runtime_template_alias(language: str, version: str) -> str:
    normalized_language = "node" if language in {"typescript", "javascript"} else language
    version_slug = re.sub(r"[^a-z0-9]+", "-", version.lower()).strip("-")
    return f"alvance-runtime-{normalized_language}-{version_slug}-amd64-{RUNTIME_RECIPE_VERSION}"


def repository_template_alias(full_name: str, commit: str, dependency_hash: str) -> str:
    repo_slug = re.sub(r"[^a-z0-9]+", "-", full_name.lower()).strip("-")[:22]
    return (
        f"alvance-repo-{repo_slug}-{commit[:10]}-{dependency_hash[:10]}-"
        f"{REPOSITORY_RECIPE_VERSION}"
    )


def _add_repository_build_steps(builder: Any, language: str, repo_path: Path) -> Any:
    language = language.lower()
    if language == "go":
        for name in ("go.mod", "go.sum"):
            if (repo_path / name).is_file():
                builder = builder.copy(name, f"/repo/{name}")
        builder = builder.run_cmd("go mod download")
        builder = builder.copy(".", "/repo")
        return builder.run_cmd("go build ./...")

    if language in {"typescript", "javascript"}:
        for name in ("package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"):
            if (repo_path / name).is_file():
                builder = builder.copy(name, f"/repo/{name}")
        builder = builder.run_cmd("npm ci")
        return builder.copy(".", "/repo")

    builder = builder.copy(".", "/repo")
    if language == "python":
        return builder.run_cmd(
            "pip install --no-cache-dir -e '.[test,dev]' || pip install --no-cache-dir -e ."
        )
    if language == "rust":
        return builder.run_cmd("cargo build --tests")
    raise ValueError(f"unsupported language: {language}")


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
