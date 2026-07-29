from __future__ import annotations

import json
import re
import tomllib
from datetime import UTC, datetime
from typing import Any

from ..github import GitHubClient
from ..models import HardFilterResult

PERMISSIVE_LICENSES = {
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC",
    "MPL-2.0",
}

JS_TEST_FRAMEWORKS = (
    "jest",
    "vitest",
    "mocha",
    "ava",
    "tap",
    "tape",
    "jasmine",
    "karma",
    "uvu",
)

NON_PROJECT_TEST_PREFIXES = {
    ".claude",
    ".github",
    "docs",
    "examples",
    "third_party",
    "vendor",
}


def _parse_github_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


class HardFilter:
    def __init__(self, github: GitHubClient, *, now: datetime | None = None) -> None:
        self.github = github
        self.now = now or datetime.now(UTC)

    def evaluate(self, repo: dict[str, Any], tree: list[dict[str, Any]]) -> HardFilterResult:
        if int(repo.get("stargazers_count", 0)) < 100:
            return HardFilterResult(False, "stars<100")

        pushed_at = repo.get("pushed_at")
        if not pushed_at or (self.now - _parse_github_datetime(pushed_at)).days > 365:
            return HardFilterResult(False, "inactive")

        license_info = repo.get("license") or {}
        if license_info.get("spdx_id") not in PERMISSIVE_LICENSES:
            return HardFilterResult(False, "license")

        language = (repo.get("language") or "").lower()
        if language not in {"go", "python", "typescript", "javascript", "rust"}:
            return HardFilterResult(False, "unsupported_language")

        if not self._has_native_tests(repo, language, tree):
            return HardFilterResult(False, "no_test_infra")
        return HardFilterResult(True, "ok")

    def _has_native_tests(
        self, repo: dict[str, Any], language: str, tree: list[dict[str, Any]]
    ) -> bool:
        return bool(test_infrastructure_evidence(self.github, repo, language, tree))


def test_infrastructure_evidence(
    github: GitHubClient,
    repo: dict[str, Any],
    language: str,
    tree: list[dict[str, Any]],
) -> list[str]:
    paths = {
        str(item["path"])
        for item in tree
        if item.get("type") == "blob" and isinstance(item.get("path"), str)
    }
    full_name = str(repo["full_name"])
    ref = str(repo.get("base_commit") or repo.get("default_branch") or "")
    language = language.lower()

    if language == "go":
        test_files = sorted(path for path in paths if path.endswith("_test.go"))
        if "go.mod" not in paths or not test_files:
            return []
        return ["file:go.mod", f"test_file:{test_files[0]}"]

    if language == "python":
        return _python_test_evidence(github, full_name, ref, paths)

    if language in {"typescript", "javascript"}:
        return _node_test_evidence(github, full_name, ref, paths)

    if language == "rust":
        return _rust_test_evidence(github, full_name, ref, paths, tree)

    return []


def _python_test_evidence(
    github: GitHubClient, full_name: str, ref: str, paths: set[str]
) -> list[str]:
    test_file = next(
        (
            path
            for path in sorted(paths)
            if _is_project_test_path(path, suffix=".py")
        ),
        "",
    )
    if test_file:
        test_index = test_file.split("/").index("tests")
        directory = "/".join(test_file.split("/")[: test_index + 1]) + "/"
        return [f"directory:{directory}", f"test_file:{test_file}"]

    if "pytest.ini" in paths:
        return ["pytest_config:pytest.ini"]
    if "conftest.py" in paths:
        return ["pytest_config:conftest.py"]

    for path in ("pyproject.toml", "setup.cfg", "tox.ini"):
        if path not in paths:
            continue
        content = github.get_file(full_name, path, ref=ref) or ""
        if _python_config_has_pytest(path, content):
            return [f"pytest_config:{path}"]

    requirement_paths = sorted(
        path
        for path in paths
        if "/" not in path
        and path.lower().startswith("requirements")
        and path.lower().endswith((".txt", ".in"))
    )
    for path in requirement_paths[:8]:
        content = github.get_file(full_name, path, ref=ref) or ""
        if any(
            re.match(r"^pytest(?:\W|$)", line.strip(), flags=re.IGNORECASE)
            for line in content.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ):
            return [f"test_dependency:{path}:pytest"]
    return []


def _python_config_has_pytest(path: str, content: str) -> bool:
    if not content.strip():
        return False
    if path == "pyproject.toml":
        try:
            payload = tomllib.loads(content)
        except tomllib.TOMLDecodeError:
            return False
        tool = payload.get("tool") or {}
        if isinstance(tool, dict) and "pytest" in tool:
            return True
        return _structured_value_contains(payload, "pytest")
    return bool(re.search(r"(^|\W)pytest(\W|$)", content, flags=re.IGNORECASE))


def _node_test_evidence(
    github: GitHubClient, full_name: str, ref: str, paths: set[str]
) -> list[str]:
    if "package.json" not in paths:
        return []
    raw = github.get_file(full_name, "package.json", ref=ref) or "{}"
    try:
        package = json.loads(raw)
    except json.JSONDecodeError:
        return []
    scripts = package.get("scripts") or {}
    if not isinstance(scripts, dict):
        return []
    test_script = str(scripts.get("test") or "").strip()
    if not test_script or "no test specified" in test_script.lower():
        return []

    dependencies: dict[str, Any] = {}
    for section in ("dependencies", "devDependencies", "peerDependencies"):
        values = package.get(section) or {}
        if isinstance(values, dict):
            dependencies.update(values)
    dependency_names = " ".join(str(name).lower() for name in dependencies)
    script_text = " ".join(str(value).lower() for value in scripts.values())
    framework = next(
        (
            name
            for name in JS_TEST_FRAMEWORKS
            if re.search(rf"(^|[^a-z0-9]){re.escape(name)}([^a-z0-9]|$)", dependency_names)
            or re.search(rf"(^|[^a-z0-9]){re.escape(name)}([^a-z0-9]|$)", script_text)
        ),
        "",
    )
    if not framework and re.search(r"\b(?:node|tsx)\s+--test\b", script_text):
        framework = "node:test"
    if not framework and "bun test" in script_text:
        framework = "bun:test"
    if not framework:
        return []
    return [
        f"test_script:package.json:{test_script[:160]}",
        f"test_framework:{framework}",
    ]


def _rust_test_evidence(
    github: GitHubClient,
    full_name: str,
    ref: str,
    paths: set[str],
    tree: list[dict[str, Any]],
) -> list[str]:
    if "Cargo.toml" not in paths:
        return []
    integration_test = next(
        (
            path
            for path in sorted(paths)
            if _is_project_test_path(path, suffix=".rs")
        ),
        "",
    )
    if integration_test:
        return ["file:Cargo.toml", f"test_file:{integration_test}"]

    cargo = github.get_file(full_name, "Cargo.toml", ref=ref) or ""
    try:
        payload = tomllib.loads(cargo)
    except tomllib.TOMLDecodeError:
        payload = {}
    if _has_nonempty_key(payload, "dev-dependencies"):
        return ["file:Cargo.toml", "test_dependency:Cargo.toml:[dev-dependencies]"]
    if isinstance(payload.get("test"), list) and payload["test"]:
        return ["file:Cargo.toml", "test_target:Cargo.toml:[[test]]"]

    source_entries = [
        item
        for item in tree
        if item.get("type") == "blob"
        and isinstance(item.get("path"), str)
        and str(item["path"]).startswith("src/")
        and str(item["path"]).endswith(".rs")
    ]
    source_entries.sort(
        key=lambda item: (
            str(item.get("path")) not in {"src/lib.rs", "src/main.rs"},
            int(item.get("size") or 0),
            str(item.get("path")),
        )
    )
    test_marker = re.compile(r"#\s*\[\s*(?:cfg\s*\(\s*test\s*\)|test)\s*\]")
    for item in source_entries[:12]:
        path = str(item["path"])
        content = github.get_file(full_name, path, ref=ref) or ""
        if test_marker.search(content):
            return ["file:Cargo.toml", f"inline_test:{path}"]
    return []


def _structured_value_contains(value: Any, needle: str) -> bool:
    if isinstance(value, dict):
        return any(
            needle in str(key).lower() or _structured_value_contains(item, needle)
            for key, item in value.items()
        )
    if isinstance(value, list):
        return any(_structured_value_contains(item, needle) for item in value)
    return needle in str(value).lower()


def _has_nonempty_key(value: Any, wanted: str) -> bool:
    if not isinstance(value, dict):
        return False
    for key, item in value.items():
        if str(key).lower() == wanted and bool(item):
            return True
        if _has_nonempty_key(item, wanted):
            return True
    return False


def _is_project_test_path(path: str, *, suffix: str) -> bool:
    parts = path.split("/")
    return (
        bool(parts)
        and parts[0] not in NON_PROJECT_TEST_PREFIXES
        and "tests" in parts[:-1]
        and path.endswith(suffix)
    )
