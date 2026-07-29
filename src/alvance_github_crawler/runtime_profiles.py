from __future__ import annotations

import hashlib
import json
import re
import shlex
from pathlib import Path

RUNTIME_RECIPE_VERSION = "v3"
REPOSITORY_RECIPE_VERSION = "v9"

DEFAULT_RUNTIME_VERSIONS = {
    "go": "1.22",
    "python": "3.11",
    "typescript": "20",
    "javascript": "20",
    "rust": "1.77",
}

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
        content = _read(repo_path / "rust-toolchain.toml") or _read(repo_path / "rust-toolchain")
        match = re.search(r"(?:channel\s*=\s*)?['\"]?(\d+\.\d+(?:\.\d+)?)", content)
        return match.group(1) if match else DEFAULT_RUNTIME_VERSIONS[language]
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


def repository_template_alias(
    full_name: str,
    commit: str,
    dependency_hash: str,
    *,
    recipe_version: str = REPOSITORY_RECIPE_VERSION,
) -> str:
    repo_slug = re.sub(r"[^a-z0-9]+", "-", full_name.lower()).strip("-")[:22]
    return f"alvance-repo-{repo_slug}-{commit[:10]}-{dependency_hash[:10]}-{recipe_version}"


def runtime_environment(language: str, version: str) -> dict[str, str]:
    language = language.lower()
    if language == "go":
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
    if language in {"python", "typescript", "javascript"}:
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


def command_with_environment(command: str, envs: dict[str, str] | None) -> str:
    """Inject envs in the shell command because E2B normalizes PATH at startup."""
    if not envs:
        return command
    assignments = " ".join(f"{key}={shlex.quote(value)}" for key, value in sorted(envs.items()))
    return f"env {assignments} sh -c {shlex.quote(command)}"


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
