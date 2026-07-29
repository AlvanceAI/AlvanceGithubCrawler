from __future__ import annotations

from datetime import UTC, datetime, timedelta

from alvance_github_crawler.screening.filters import HardFilter
from alvance_github_crawler.screening.filters import (
    test_infrastructure_evidence as collect_test_evidence,
)


class FakeGitHub:
    def __init__(self, files: dict[str, str] | None = None) -> None:
        self.files = files or {}

    def get_file(self, full_name: str, path: str, *, ref: str | None = None) -> str | None:
        return self.files.get(path)


def repo(language: str = "Go") -> dict[str, object]:
    return {
        "full_name": "owner/repo",
        "default_branch": "main",
        "base_commit": "abc",
        "language": language,
        "stargazers_count": 500,
        "pushed_at": datetime.now(UTC).isoformat(),
        "license": {"spdx_id": "MIT"},
    }


def blobs(*paths: str) -> list[dict[str, str]]:
    return [{"type": "blob", "path": path} for path in paths]


def test_go_requires_module_and_test_file() -> None:
    result = HardFilter(FakeGitHub()).evaluate(repo(), blobs("go.mod", "pkg/a_test.go"))
    assert result.ok

    result = HardFilter(FakeGitHub()).evaluate(repo(), blobs("go.mod", "pkg/a.go"))
    assert not result.ok
    assert result.reason == "no_test_infra"


def test_python_marker_must_configure_pytest() -> None:
    github = FakeGitHub({"pyproject.toml": "[tool.pytest.ini_options]\naddopts = '-q'"})
    result = HardFilter(github).evaluate(repo("Python"), blobs("pyproject.toml"))
    assert result.ok

    github = FakeGitHub({"pyproject.toml": "[project]\nname = 'demo'"})
    result = HardFilter(github).evaluate(repo("Python"), blobs("pyproject.toml"))
    assert not result.ok


def test_python_accepts_tests_directory() -> None:
    result = HardFilter(FakeGitHub()).evaluate(
        repo("Python"), blobs("pyproject.toml", "tests/test_api.py")
    )
    assert result.ok

    hidden_tool_tests = HardFilter(FakeGitHub()).evaluate(
        repo("Python"), blobs("pyproject.toml", ".claude/skills/check/tests/test_tool.py")
    )
    assert not hidden_tool_tests.ok


def test_javascript_detects_jest_or_vitest() -> None:
    github = FakeGitHub(
        {"package.json": '{"scripts":{"test":"vitest run"},"devDependencies":{"vitest":"1"}}'}
    )
    result = HardFilter(github).evaluate(repo("TypeScript"), blobs("package.json"))
    assert result.ok

    no_test_script = FakeGitHub({"package.json": '{"devDependencies":{"jest":"1"}}'})
    result = HardFilter(no_test_script).evaluate(repo("JavaScript"), blobs("package.json"))
    assert not result.ok


def test_rust_requires_dev_dependencies() -> None:
    github = FakeGitHub({"Cargo.toml": "[dev-dependencies]\nproptest = '1'"})
    result = HardFilter(github).evaluate(repo("Rust"), blobs("Cargo.toml"))
    assert result.ok

    evidence = collect_test_evidence(
        FakeGitHub(), repo("Rust"), "rust", blobs("Cargo.toml", "crates/api/tests/api.rs")
    )
    assert evidence == ["file:Cargo.toml", "test_file:crates/api/tests/api.rs"]


def test_rejects_inactive_or_non_permissive_repo() -> None:
    stale = repo()
    stale["pushed_at"] = (datetime.now(UTC) - timedelta(days=366)).isoformat()
    assert (
        HardFilter(FakeGitHub()).evaluate(stale, blobs("go.mod", "a_test.go")).reason == "inactive"
    )

    non_permissive = repo()
    non_permissive["license"] = {"spdx_id": "GPL-3.0"}
    assert (
        HardFilter(FakeGitHub()).evaluate(non_permissive, blobs("go.mod", "a_test.go")).reason
        == "license"
    )
