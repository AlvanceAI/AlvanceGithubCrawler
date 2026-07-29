from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from .github import GitHubClient
from .models import HardFilterResult

PERMISSIVE_LICENSES = {
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC",
    "MPL-2.0",
}


def _parse_github_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


class HardFilter:
    def __init__(self, github: GitHubClient, *, now: datetime | None = None) -> None:
        self.github = github
        self.now = now or datetime.now(timezone.utc)

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
        paths = {
            item["path"]
            for item in tree
            if item.get("type") == "blob" and isinstance(item.get("path"), str)
        }
        full_name = repo["full_name"]
        ref = repo.get("base_commit") or repo.get("default_branch")

        if language == "go":
            return "go.mod" in paths and any(path.endswith("_test.go") for path in paths)

        if language == "python":
            if "pytest.ini" in paths:
                return True
            for marker in ("pyproject.toml", "setup.cfg"):
                if marker in paths:
                    content = self.github.get_file(full_name, marker, ref=ref) or ""
                    lowered = content.lower()
                    if "pytest" in lowered or "[tool.pytest" in lowered:
                        return True
            return False

        if language in {"typescript", "javascript"}:
            if "package.json" not in paths:
                return False
            raw = self.github.get_file(full_name, "package.json", ref=ref) or "{}"
            try:
                package = json.loads(raw)
            except json.JSONDecodeError:
                return False
            dependencies = {
                **(package.get("dependencies") or {}),
                **(package.get("devDependencies") or {}),
            }
            scripts = " ".join(str(value) for value in (package.get("scripts") or {}).values())
            signals = " ".join([*dependencies.keys(), scripts]).lower()
            return "jest" in signals or "vitest" in signals

        if language == "rust":
            if "Cargo.toml" not in paths:
                return False
            cargo = self.github.get_file(full_name, "Cargo.toml", ref=ref) or ""
            return "[dev-dependencies" in cargo.lower()

        return False
