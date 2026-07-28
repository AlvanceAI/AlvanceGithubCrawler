from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from .models import BuildResult

DOCKERFILE_TEMPLATES = {
    "go": """FROM golang:1.22
RUN apt-get update && apt-get install -y --no-install-recommends time && rm -rf /var/lib/apt/lists/*
WORKDIR /repo
COPY . .
RUN go mod download && go build ./...
""",
    "python": """FROM python:3.11
RUN apt-get update && apt-get install -y --no-install-recommends time && rm -rf /var/lib/apt/lists/*
WORKDIR /repo
COPY . .
RUN pip install --no-cache-dir -e '.[test,dev]' || pip install --no-cache-dir -e .
""",
    "typescript": """FROM node:20
RUN apt-get update && apt-get install -y --no-install-recommends time && rm -rf /var/lib/apt/lists/*
WORKDIR /repo
COPY . .
RUN npm ci
""",
    "javascript": """FROM node:20
RUN apt-get update && apt-get install -y --no-install-recommends time && rm -rf /var/lib/apt/lists/*
WORKDIR /repo
COPY . .
RUN npm ci
""",
    "rust": """FROM rust:1.77
RUN apt-get update && apt-get install -y --no-install-recommends time && rm -rf /var/lib/apt/lists/*
WORKDIR /repo
COPY . .
RUN cargo build --tests
""",
}

TEST_COMMANDS = {
    "go": "go test ./...",
    "python": "python -m pytest -x -q",
    "typescript": "CI=1 npm test",
    "javascript": "CI=1 npm test",
    "rust": "cargo test",
}


def dockerfile_for(language: str, repo_path: Path | None = None) -> str:
    language = language.lower()
    try:
        dockerfile = DOCKERFILE_TEMPLATES[language]
    except KeyError as exc:
        raise ValueError(f"unsupported language: {language}") from exc
    if repo_path is None:
        return dockerfile
    base_image = _detect_base_image(language, repo_path)
    first_line, rest = dockerfile.split("\n", 1)
    return f"FROM {base_image}\n{rest}" if first_line.startswith("FROM ") else dockerfile


def test_command_for(language: str, repo_path: Path | None = None) -> str:
    language = language.lower()
    if language in {"typescript", "javascript"} and repo_path is not None:
        package_path = repo_path / "package.json"
        try:
            package = json.loads(package_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            package = {}
        scripts = package.get("scripts") or {}
        if scripts.get("test"):
            return "CI=1 npm test"
        dependencies = {
            **(package.get("dependencies") or {}),
            **(package.get("devDependencies") or {}),
        }
        if "vitest" in dependencies:
            return "npx vitest run"
        if "jest" in dependencies:
            return "npx jest --ci"
    try:
        return TEST_COMMANDS[language]
    except KeyError as exc:
        raise ValueError(f"unsupported language: {language}") from exc


def image_tag(repo: dict[str, Any], base_commit: str) -> str:
    name = re.sub(r"[^a-z0-9_.-]+", "-", repo["full_name"].lower()).strip("-.")
    digest = hashlib.sha256(f"{repo['full_name']}@{base_commit}".encode()).hexdigest()[:10]
    return f"alvance-repo:{name[:80]}-{digest}"


class DockerBuildVerifier:
    def __init__(self, *, timeout_s: int = 600) -> None:
        self.timeout_s = timeout_s

    def verify(
        self, repo: dict[str, Any], base_commit: str, repo_path: Path
    ) -> BuildResult:
        language = (repo.get("language") or "").lower()
        dockerfile = dockerfile_for(language, repo_path)
        test_cmd = test_command_for(language, repo_path)
        tag = image_tag(repo, base_commit)

        try:
            build = subprocess.run(
                ["docker", "build", "-f", "-", "-t", tag, "."],
                cwd=repo_path,
                input=dockerfile,
                text=True,
                capture_output=True,
                timeout=self.timeout_s,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            return BuildResult(
                ok=False,
                reason="build_timeout",
                dockerfile=dockerfile,
                test_cmd=test_cmd,
                log_tail=_timeout_tail(exc),
            )
        if build.returncode != 0:
            return BuildResult(
                ok=False,
                reason="build_fail",
                dockerfile=dockerfile,
                test_cmd=test_cmd,
                log_tail=_tail(build.stdout, build.stderr),
            )

        try:
            offline_test = subprocess.run(
                ["docker", "run", "--rm", "--network=none", tag, "sh", "-lc", test_cmd],
                text=True,
                capture_output=True,
                timeout=self.timeout_s,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            return BuildResult(
                ok=False,
                reason="offline_test_timeout",
                image=tag,
                dockerfile=dockerfile,
                test_cmd=test_cmd,
                log_tail=_timeout_tail(exc),
            )
        if offline_test.returncode != 0:
            return BuildResult(
                ok=False,
                reason="offline_test_fail",
                image=tag,
                dockerfile=dockerfile,
                test_cmd=test_cmd,
                log_tail=_tail(offline_test.stdout, offline_test.stderr),
            )
        return BuildResult(
            ok=True,
            reason="ok",
            image=tag,
            dockerfile=dockerfile,
            test_cmd=test_cmd,
            log_tail=_tail(offline_test.stdout, offline_test.stderr),
        )

    @staticmethod
    def remove_image(tag: str) -> None:
        if not tag:
            return
        try:
            subprocess.run(
                ["docker", "image", "rm", "-f", tag],
                text=True,
                capture_output=True,
                timeout=120,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            pass


def _tail(*parts: str | None, size: int = 4_000) -> str:
    return "\n".join(part for part in parts if part)[-size:]


def _timeout_tail(exc: subprocess.TimeoutExpired) -> str:
    stdout = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else exc.stdout
    stderr = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else exc.stderr
    return _tail(stdout, stderr)


def _detect_base_image(language: str, repo_path: Path) -> str:
    if language == "go":
        content = _read(repo_path / "go.mod")
        match = re.search(r"^go\s+(\d+\.\d+(?:\.\d+)?)\s*$", content, re.MULTILINE)
        return f"golang:{match.group(1)}" if match else "golang:1.22"

    if language == "python":
        content = _read(repo_path / "pyproject.toml")
        match = re.search(r"requires-python\s*=\s*['\"][^'\"]*?(\d+\.\d+)", content)
        return f"python:{match.group(1)}" if match else "python:3.11"

    if language in {"typescript", "javascript"}:
        try:
            package = json.loads(_read(repo_path / "package.json") or "{}")
        except json.JSONDecodeError:
            package = {}
        engine = str((package.get("engines") or {}).get("node", ""))
        majors = [int(value) for value in re.findall(r"(?<!\d)(\d{2})(?:\.\d+)?", engine)]
        major = max(20, min(majors)) if majors else 20
        return f"node:{major}"

    if language == "rust":
        content = _read(repo_path / "rust-toolchain.toml") or _read(
            repo_path / "rust-toolchain"
        )
        match = re.search(r"(?:channel\s*=\s*)?['\"]?(\d+\.\d+(?:\.\d+)?)", content)
        return f"rust:{match.group(1)}" if match else "rust:1.77"

    raise ValueError(f"unsupported language: {language}")


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
