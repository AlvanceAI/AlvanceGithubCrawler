from __future__ import annotations

import hashlib
import json
import re
import shlex
import tomllib
from pathlib import Path

from packaging.specifiers import InvalidSpecifier, SpecifierSet

RUNTIME_RECIPE_VERSION = "v3"
REPOSITORY_RECIPE_VERSION = "v17"

DEFAULT_RUNTIME_VERSIONS = {
    "go": "1.22",
    "python": "3.11",
    "typescript": "20",
    "javascript": "20",
    "rust": "1.77",
}

PYTHON_RUNTIME_CANDIDATES = ("3.11", "3.12", "3.13", "3.10", "3.9", "3.8")

DEPENDENCY_FILES = {
    "go": ("go.mod", "go.sum", "go.work", "go.work.sum"),
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


def detect_runtime_version(language: str, repo_path: Path) -> str:
    language = language.lower()
    if language == "go":
        match = re.search(
            r"^go\s+(\d+\.\d+(?:\.\d+)?)\s*$",
            _read(repo_path / "go.mod"),
            re.MULTILINE,
        )
        version = match.group(1) if match else DEFAULT_RUNTIME_VERSIONS[language]
        return normalize_go_toolchain_version(version)
    if language == "python":
        match = re.search(
            r"requires-python\s*=\s*['\"]([^'\"]+)['\"]",
            _read(repo_path / "pyproject.toml"),
        )
        return select_python_runtime(match.group(1) if match else "")
    if language in {"typescript", "javascript"}:
        try:
            package = json.loads(_read(repo_path / "package.json") or "{}")
        except json.JSONDecodeError:
            package = {}
        engine = str((package.get("engines") or {}).get("node", ""))
        majors = [int(value) for value in re.findall(r"(?<!\d)(\d{2})(?:\.\d+)?", engine)]
        return str(max(20, min(majors))) if majors else DEFAULT_RUNTIME_VERSIONS[language]
    if language == "rust":
        return detect_rust_runtime(repo_path)
    raise ValueError(f"unsupported language: {language}")


def select_python_runtime(requirement: str) -> str:
    if not requirement.strip():
        return DEFAULT_RUNTIME_VERSIONS["python"]
    try:
        specifier = SpecifierSet(requirement)
    except InvalidSpecifier:
        return DEFAULT_RUNTIME_VERSIONS["python"]
    for version in PYTHON_RUNTIME_CANDIDATES:
        if specifier.contains(version, prereleases=False):
            return version
    raise ValueError(f"no supported Python runtime satisfies requires-python={requirement!r}")


def normalize_go_toolchain_version(version: str) -> str:
    """Turn a Go language version into the concrete toolchain name E2B needs."""
    return f"{version}.0" if re.fullmatch(r"\d+\.\d+", version) else version


def detect_rust_runtime(repo_path: Path) -> str:
    channel = ""
    toolchain_path = repo_path / "rust-toolchain.toml"
    if toolchain_path.is_file():
        try:
            toolchain = tomllib.loads(_read(toolchain_path))
        except tomllib.TOMLDecodeError:
            toolchain = {}
        channel = str((toolchain.get("toolchain") or {}).get("channel") or "").strip()
    else:
        channel = _read(repo_path / "rust-toolchain").strip()

    if re.fullmatch(r"\d+\.\d+(?:\.\d+)?", channel):
        return channel

    try:
        cargo = tomllib.loads(_read(repo_path / "Cargo.toml"))
    except tomllib.TOMLDecodeError:
        cargo = {}
    workspace_version = ((cargo.get("workspace") or {}).get("package") or {}).get(
        "rust-version"
    )
    package_version = (cargo.get("package") or {}).get("rust-version")
    rust_version = str(workspace_version or package_version or "").strip()
    if re.fullmatch(r"\d+\.\d+(?:\.\d+)?", rust_version):
        return rust_version
    if channel in {"stable", "beta", "nightly"}:
        return channel
    return DEFAULT_RUNTIME_VERSIONS["rust"]


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


def runtime_template_alias(
    language: str,
    version: str,
    *,
    cpu_count: int = 1,
    memory_mb: int = 1_024,
) -> str:
    normalized_language = "node" if language in {"typescript", "javascript"} else language
    if normalized_language == "go":
        version = normalize_go_toolchain_version(version)
    version_slug = re.sub(r"[^a-z0-9]+", "-", version.lower()).strip("-")
    resources = _resource_alias_suffix(cpu_count, memory_mb)
    return (
        f"alvance-runtime-{normalized_language}-{version_slug}-amd64"
        f"{resources}-{RUNTIME_RECIPE_VERSION}"
    )


def repository_template_alias(
    full_name: str,
    commit: str,
    dependency_hash: str,
    *,
    recipe_version: str = REPOSITORY_RECIPE_VERSION,
    cpu_count: int = 1,
    memory_mb: int = 1_024,
) -> str:
    name_hash = hashlib.sha256(full_name.lower().encode()).hexdigest()[:8]
    resources = _resource_alias_suffix(cpu_count, memory_mb, include_default=True)
    suffix = f"-{name_hash}-{commit[:10]}-{dependency_hash[:10]}{resources}-{recipe_version}"
    max_slug_length = max(1, min(22, 63 - len("alvance-repo-") - len(suffix)))
    repo_slug = re.sub(r"[^a-z0-9]+", "-", full_name.lower()).strip("-")[:max_slug_length]
    return f"alvance-repo-{repo_slug}{suffix}"


def _resource_alias_suffix(
    cpu_count: int,
    memory_mb: int,
    *,
    include_default: bool = False,
) -> str:
    if not include_default and cpu_count == 1 and memory_mb == 1_024:
        return ""
    return f"-c{cpu_count}-m{memory_mb}"


def runtime_environment(language: str, version: str) -> dict[str, str]:
    language = language.lower()
    if language == "go":
        version = normalize_go_toolchain_version(version)
        return {
            "PATH": (
                "/usr/local/go/bin:/go/bin:/usr/local/sbin:/usr/local/bin:"
                "/usr/sbin:/usr/bin:/sbin:/bin"
            ),
            "HOME": "/root",
            "GOPATH": "/go",
            "GOMODCACHE": "/go/pkg/mod",
            "GOCACHE": "/root/.cache/go-build",
            "GOPROXY": "https://goproxy.cn,direct",
            "GOTOOLCHAIN": f"go{version}+auto",
        }
    if language == "python":
        return {
            "PATH": "/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin",
            "HOME": "/home/user",
        }
    if language in {"typescript", "javascript"}:
        return {
            "PATH": "/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin",
            "HOME": "/root",
        }
    if language == "rust":
        return {
            "PATH": (
                "/usr/local/cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            ),
            "HOME": "/root",
            "CARGO_HOME": "/usr/local/cargo",
            "RUSTUP_HOME": "/usr/local/rustup",
        }
    raise ValueError(f"unsupported language: {language}")


def execution_user(language: str) -> str:
    """Return the user whose filesystem semantics define repository tests."""
    return "user" if language.lower() == "python" else "root"


def command_with_environment(command: str, envs: dict[str, str] | None) -> str:
    """Inject envs in the shell command because E2B normalizes PATH at startup."""
    if not envs:
        return command
    assignments = " ".join(f"{key}={shlex.quote(value)}" for key, value in sorted(envs.items()))
    return f"env {assignments} sh -c {shlex.quote(command)}"


def command_as_user(command: str, user: str) -> str:
    if user == "root":
        return command
    return f"runuser -u {shlex.quote(user)} -- {command}"


def command_with_timeout(command: str, timeout_s: int) -> str:
    """Enforce the command budget inside the sandbox, independent of SDK streaming."""
    return f"timeout --signal=TERM --kill-after=10s {timeout_s}s sh -c {shlex.quote(command)}"


def render_runtime_dockerfile(language: str, version: str) -> str:
    """Render the legacy local-Docker runtime description used by tests and fallback."""
    apt = (
        "RUN apt-get update && apt-get install -y --no-install-recommends "
        "time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*"
    )
    language = language.lower()
    image = {
        "go": "golang:1.22",
        "python": f"python:{version}",
        "typescript": f"node:{version}",
        "javascript": f"node:{version}",
        "rust": f"rust:{version}",
    }.get(language)
    if image is None:
        raise ValueError(f"unsupported language: {language}")
    envs = runtime_environment(language, version)
    env_lines = "\n".join(f"ENV {key}={value}" for key, value in envs.items())
    probe = {
        "go": "go version",
        "python": "python --version && pip --version",
        "typescript": "node --version && npm --version",
        "javascript": "node --version && npm --version",
        "rust": "rustc --version && cargo --version",
    }[language]
    return f"FROM {image}\n{env_lines}\n{apt}\nRUN {probe}\nWORKDIR /app\n"


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
