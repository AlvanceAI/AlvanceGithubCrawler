from __future__ import annotations

import json
import re
import shlex
from pathlib import Path

from .profiles import normalize_go_toolchain_version
from .python import python_install_commands

SYSTEM_PACKAGES_COMMAND = (
    "apt-get update && apt-get install -y --no-install-recommends "
    "time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*"
)


def runtime_base_image(language: str, version: str) -> str:
    """Return the version-pinned public image used by E2B and Harbor rebuilds."""
    language = language.lower()
    if language == "go":
        # Go 1.22 is the local bootstrap. Newer modules opt into Go's automatic
        # toolchain selection through their go.mod metadata.
        return "docker.io/library/golang:1.22"
    if language == "python":
        return f"docker.io/library/python:{version}"
    if language in {"typescript", "javascript"}:
        return f"docker.io/library/node:{version}"
    if language == "rust":
        return f"docker.io/library/rust:{version}"
    raise ValueError(f"unsupported language: {language}")


def runtime_probe_command(language: str) -> str:
    language = language.lower()
    try:
        return {
            "go": "/usr/local/go/bin/go version",
            "python": "/usr/local/bin/python --version && /usr/local/bin/pip --version",
            "typescript": "/usr/local/bin/node --version && /usr/local/bin/npm --version",
            "javascript": "/usr/local/bin/node --version && /usr/local/bin/npm --version",
            "rust": (
                "/usr/local/cargo/bin/rustc --version "
                "&& /usr/local/cargo/bin/cargo --version"
            ),
        }[language]
    except KeyError as exc:
        raise ValueError(f"unsupported language: {language}") from exc


def repository_dependency_commands(
    language: str,
    repo_path: Path | None = None,
) -> tuple[str, ...]:
    """Return the repository setup commands shared by E2B and Dockerfile builds."""
    language = language.lower()
    if language == "go":
        return (
            "/usr/local/go/bin/go mod download",
            "/usr/local/go/bin/go build ./...",
        )
    if language in {"typescript", "javascript"}:
        if repo_path is None:
            return ("/usr/local/bin/npm ci",)
        if (repo_path / "package-lock.json").is_file() or (
            repo_path / "npm-shrinkwrap.json"
        ).is_file():
            return ("/usr/local/bin/npm ci",)

        package_manager = _node_package_manager(repo_path)
        if (repo_path / "pnpm-lock.yaml").is_file() or package_manager == "pnpm":
            return (
                "/usr/local/bin/corepack enable && "
                "/usr/local/bin/pnpm install --frozen-lockfile",
            )
        if (repo_path / "yarn.lock").is_file() or package_manager == "yarn":
            immutable = _uses_yarn_berry(repo_path)
            flag = "--immutable" if immutable else "--frozen-lockfile"
            return (
                "/usr/local/bin/corepack enable && "
                f"/usr/local/bin/yarn install {flag}",
            )
        raise UnsupportedDependencyError(
            "Node repository has no supported lockfile "
            "(package-lock.json, npm-shrinkwrap.json, pnpm-lock.yaml, or yarn.lock)"
        )
    if language == "python":
        if repo_path is None:
            # Only used to read pre-v0.3 candidate records. Production and migration
            # always persist the resolver's exact repository-specific command list.
            return (
                "/usr/local/bin/pip install --no-cache-dir pytest",
                "/usr/local/bin/pip install --no-cache-dir -e .",
            )
        return tuple(python_install_commands(repo_path))
    if language == "rust":
        return ("/usr/local/cargo/bin/cargo build --tests",)
    raise ValueError(f"unsupported language: {language}")


def repository_checkout_command(
    full_name: str,
    base_commit: str,
    default_branch: str,
    *,
    source_tree: str = "",
) -> str:
    repository_url = shlex.quote(f"https://github.com/{full_name}.git")
    commit = shlex.quote(base_commit)
    branch = shlex.quote(default_branch)
    command = (
        "rm -rf /app && mkdir -p /app && git init /app && cd /app "
        f"&& git remote add origin {repository_url} "
        f"&& git fetch --depth=1 origin {commit} "
        "&& git checkout --detach FETCH_HEAD "
        "&& git submodule update --init --recursive "
        f"&& git update-ref refs/remotes/origin/{branch} HEAD "
        f'&& test "$(git rev-parse HEAD)" = {commit}'
    )
    if source_tree:
        tree = shlex.quote(source_tree)
        command += f' && test "$(git rev-parse HEAD^{{tree}})" = {tree}'
    return command


def repository_finalize_commands(language: str) -> tuple[str, ...]:
    commands = ['test -z "$(git status --porcelain)"']
    if language.lower() == "python":
        commands.append("chown -R user:user /app")
    return tuple(commands)


class UnsupportedDependencyError(ValueError):
    """A deterministic dependency installation recipe cannot be produced."""


def _node_package_manager(repo_path: Path) -> str:
    try:
        package = json.loads((repo_path / "package.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    value = str(package.get("packageManager") or "").strip().lower()
    return value.split("@", 1)[0]


def _uses_yarn_berry(repo_path: Path) -> bool:
    if (repo_path / ".yarnrc.yml").is_file() or (repo_path / ".yarn" / "releases").is_dir():
        return True
    try:
        package = json.loads((repo_path / "package.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    value = str(package.get("packageManager") or "").strip().lower()
    match = re.match(r"yarn@(\d+)", value)
    return bool(match and int(match.group(1)) >= 2)


def normalized_runtime_version(language: str, version: str) -> str:
    if language.lower() == "go":
        return normalize_go_toolchain_version(version)
    return version
