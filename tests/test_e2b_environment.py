from __future__ import annotations

import sys
from types import SimpleNamespace

from alvance_github_crawler.e2b_environment import (
    E2BOfflineVerifier,
    _add_repository_build_steps,
    detect_runtime_version,
    go_local_dependency_paths,
    hash_dependency_manifests,
    render_runtime_dockerfile,
    repository_recipe_version,
    repository_template_alias,
    runtime_template_alias,
)


class _CommandFailure(Exception):
    def __init__(self) -> None:
        super().__init__("tests failed")
        self.exit_code = 2
        self.stdout = "test output"
        self.stderr = "test failure"


def test_offline_verifier_passes_envs_and_records_command_failure(monkeypatch) -> None:
    created: dict[str, object] = {}

    class Commands:
        def run(self, command: str, *, user: str, timeout: int):
            assert command.startswith("env ")
            assert "PATH=" in command
            assert "go test ./..." in command
            assert user == "root"
            assert timeout == 600
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


def test_go_runtime_and_template_recipe(tmp_path) -> None:
    (tmp_path / "go.mod").write_text(
        "module example.com/demo\n\ngo 1.26.5\n", encoding="utf-8"
    )
    version = detect_runtime_version("go", tmp_path)
    assert version == "1.26.5"
    dockerfile = render_runtime_dockerfile("go", version)
    assert "GOTOOLCHAIN=go1.26.5+auto" in dockerfile
    assert "PATH=/usr/local/go/bin" in dockerfile
    assert runtime_template_alias("go", version) == (
        "alvance-runtime-go-1-26-5-amd64-v3"
    )


def test_dependency_hash_changes_with_lockfile(tmp_path) -> None:
    (tmp_path / "package.json").write_text('{"name":"demo"}', encoding="utf-8")
    first = hash_dependency_manifests("typescript", tmp_path)
    (tmp_path / "package-lock.json").write_text("{}", encoding="utf-8")
    second = hash_dependency_manifests("typescript", tmp_path)
    assert first != second


def test_go_local_dependency_paths(tmp_path) -> None:
    (tmp_path / "internal" / "mintcore").mkdir(parents=True)
    (tmp_path / "tools").mkdir()
    (tmp_path / "go.mod").write_text(
        "replace example.com/mintcore => ./internal/mintcore\n",
        encoding="utf-8",
    )
    (tmp_path / "go.work").write_text(
        "use (\n\t./tools\n\t../outside\n)\n",
        encoding="utf-8",
    )

    assert go_local_dependency_paths(tmp_path) == ["internal/mintcore", "tools"]
    assert repository_recipe_version("go", tmp_path) == "v6"


def test_standard_repository_recipe_stays_on_v4(tmp_path) -> None:
    (tmp_path / "go.mod").write_text("module example.com/demo\n", encoding="utf-8")
    assert repository_recipe_version("go", tmp_path) == "v4"


def test_go_repository_clears_dependency_staging_before_full_copy(tmp_path) -> None:
    (tmp_path / "internal" / "mintcore").mkdir(parents=True)
    (tmp_path / "go.mod").write_text(
        "replace example.com/mintcore => ./internal/mintcore\n",
        encoding="utf-8",
    )

    class Builder:
        def __init__(self) -> None:
            self.events: list[tuple[str, str]] = []

        def copy(self, source: str, destination: str):
            self.events.append(("copy", f"{source} {destination}"))
            return self

        def run_cmd(self, command: str, *, user: str):
            assert user == "root"
            self.events.append(("run", command))
            return self

    builder = _add_repository_build_steps(Builder(), "go", tmp_path)
    cleanup_index = builder.events.index(
        ("run", "find /repo -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +")
    )
    full_copy_index = builder.events.index(("copy", ". /repo"))
    assert cleanup_index < full_copy_index


def test_repository_alias_is_bounded() -> None:
    alias = repository_template_alias(
        "organization-with-a-very-long-name/repository-with-a-very-long-name",
        "a" * 40,
        "b" * 16,
    )
    assert len(alias) <= 63
