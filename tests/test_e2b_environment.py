from __future__ import annotations

import sys
from types import SimpleNamespace

from alvance_github_crawler.e2b_environment import (
    E2BOfflineVerifier,
    _add_repository_build_steps,
    detect_runtime_version,
    hash_dependency_manifests,
    render_runtime_dockerfile,
    repository_template_alias,
    runtime_environment,
    runtime_template_alias,
    select_python_runtime,
)


class _CommandFailure(Exception):
    def __init__(self) -> None:
        super().__init__("tests failed")
        self.exit_code = 2
        self.stdout = "test output"
        self.stderr = "test failure"


class TimeoutException(Exception):
    pass


def test_offline_verifier_passes_envs_and_records_command_failure(monkeypatch) -> None:
    created: dict[str, object] = {}

    class Commands:
        def run(self, command: str, *, user: str, timeout: int):
            assert command.startswith("env ")
            assert "PATH=" in command
            assert "timeout --signal=TERM --kill-after=10s 600s" in command
            assert "go test ./..." in command
            assert user == "root"
            assert timeout == 630
            raise _CommandFailure

    class Sandbox:
        commands = Commands()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        @classmethod
        def create(cls, **kwargs):
            created.update(kwargs)
            return cls()

    monkeypatch.setitem(sys.modules, "e2b", SimpleNamespace(Sandbox=Sandbox))
    envs = {
        "PATH": "/usr/local/go/bin:/usr/bin",
        "GOTOOLCHAIN": "go1.26.5+auto",
    }
    result = E2BOfflineVerifier("test-key").verify(
        "repo-template",
        "go test ./...",
        envs=envs,
    )

    assert created["allow_internet_access"] is False
    assert created["envs"] == envs
    assert not result.ok
    assert result.reason == "offline_test_fail"
    assert result.exit_code == 2
    assert result.stderr_tail == "test failure"


def test_offline_verifier_records_timeout(monkeypatch) -> None:
    class Commands:
        def run(self, command: str, *, user: str, timeout: int):
            raise TimeoutException("request timed out")

    class Sandbox:
        commands = Commands()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        @classmethod
        def create(cls, **kwargs):
            return cls()

    monkeypatch.setitem(sys.modules, "e2b", SimpleNamespace(Sandbox=Sandbox))
    result = E2BOfflineVerifier("test-key").verify(
        "repo-template",
        "go test ./...",
        envs={"PATH": "/usr/local/go/bin:/usr/bin"},
    )

    assert not result.ok
    assert result.reason == "offline_test_timeout"
    assert result.exit_code == -1
    assert result.stderr_tail == "request timed out"


def test_offline_verifier_runs_as_selected_user(monkeypatch) -> None:
    observed: dict[str, object] = {}

    class Result:
        exit_code = 0
        stdout = ""
        stderr = ""

    class Commands:
        def run(self, command: str, *, user: str, timeout: int):
            observed.update(command=command, user=user, timeout=timeout)
            return Result()

    class Sandbox:
        commands = Commands()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        @classmethod
        def create(cls, **kwargs):
            return cls()

    monkeypatch.setitem(sys.modules, "e2b", SimpleNamespace(Sandbox=Sandbox))
    result = E2BOfflineVerifier("test-key").verify(
        "repo-template",
        "python -m pytest -q",
        envs=runtime_environment("python", "3.11"),
        user="user",
    )

    assert result.ok
    assert observed["user"] == "user"
    assert "HOME=/home/user" in str(observed["command"])


def test_offline_verifier_classifies_shell_timeout(monkeypatch) -> None:
    class Result:
        exit_code = 124
        stdout = ""
        stderr = ""

    class Commands:
        def run(self, command: str, *, user: str, timeout: int):
            return Result()

    class Sandbox:
        commands = Commands()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        @classmethod
        def create(cls, **kwargs):
            return cls()

    monkeypatch.setitem(sys.modules, "e2b", SimpleNamespace(Sandbox=Sandbox))
    result = E2BOfflineVerifier("test-key").verify("repo-template", "pytest")

    assert not result.ok
    assert result.reason == "offline_test_timeout"
    assert result.exit_code == 124


def test_go_runtime_and_template_recipe(tmp_path) -> None:
    (tmp_path / "go.mod").write_text("module example.com/demo\n\ngo 1.26.5\n", encoding="utf-8")
    version = detect_runtime_version("go", tmp_path)
    assert version == "1.26.5"
    dockerfile = render_runtime_dockerfile("go", version)
    assert "GOTOOLCHAIN=go1.26.5+auto" in dockerfile
    assert "PATH=/usr/local/go/bin" in dockerfile
    assert runtime_template_alias("go", version) == ("alvance-runtime-go-1-26-5-amd64-v3")


def test_dependency_hash_changes_with_lockfile(tmp_path) -> None:
    (tmp_path / "package.json").write_text('{"name":"demo"}', encoding="utf-8")
    first = hash_dependency_manifests("typescript", tmp_path)
    (tmp_path / "package-lock.json").write_text("{}", encoding="utf-8")
    second = hash_dependency_manifests("typescript", tmp_path)
    assert first != second


def test_python_runtime_prefers_stable_default_within_constraints(tmp_path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nrequires-python = ">=3.7"\n',
        encoding="utf-8",
    )
    assert detect_runtime_version("python", tmp_path) == "3.11"
    assert select_python_runtime(">=3.12,<4") == "3.12"
    assert select_python_runtime(">=3.8,<3.11") == "3.10"
    assert runtime_environment("python", "3.11")["HOME"] == "/home/user"


def test_repository_build_keeps_exact_git_commit() -> None:
    class Builder:
        def __init__(self) -> None:
            self.events: list[tuple[str, str]] = []

        def run_cmd(self, command: str, *, user: str):
            assert user == "root"
            self.events.append(("run", command))
            return self

        def set_workdir(self, workdir: str):
            self.events.append(("workdir", workdir))
            return self

    commit = "a" * 40
    builder = _add_repository_build_steps(
        Builder(),
        "go",
        "owner/repo",
        commit,
    )
    clone_command = builder.events[0][1]
    assert "git init /app" in clone_command
    assert f"git fetch --depth=1 origin {commit}" in clone_command
    assert ("workdir", "/app") in builder.events
    assert "refs/remotes/origin/main" in clone_command
    assert ("run", "/usr/local/go/bin/go mod download") in builder.events
    assert builder.events[-1] == ("run", 'test -z "$(git status --porcelain)"')


def test_python_repository_becomes_owned_by_execution_user(tmp_path) -> None:
    class Builder:
        def __init__(self) -> None:
            self.events: list[tuple[str, str]] = []

        def run_cmd(self, command: str, *, user: str):
            assert user == "root"
            self.events.append(("run", command))
            return self

        def set_workdir(self, workdir: str):
            self.events.append(("workdir", workdir))
            return self

    (tmp_path / "pyproject.toml").write_text('[project]\nname = "demo"\n', encoding="utf-8")
    builder = _add_repository_build_steps(
        Builder(),
        "python",
        "owner/repo",
        "a" * 40,
        repo_path=tmp_path,
    )

    assert builder.events[-2:] == [
        ("run", 'test -z "$(git status --porcelain)"'),
        ("run", "chown -R user:user /app"),
    ]


def test_repository_alias_is_bounded() -> None:
    alias = repository_template_alias(
        "organization-with-a-very-long-name/repository-with-a-very-long-name",
        "a" * 40,
        "b" * 16,
    )
    assert len(alias) <= 63
    assert alias.endswith("-v10")
