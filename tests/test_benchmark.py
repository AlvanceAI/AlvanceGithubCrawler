from __future__ import annotations

import sys
from types import SimpleNamespace

from alvance_github_crawler.e2b.benchmark import (
    E2BBenchmark,
    parse_max_rss,
    subset_test_command,
    summarize_runs,
)
from alvance_github_crawler.models import BenchmarkRun
from alvance_github_crawler.runtime.build import dockerfile_for
from alvance_github_crawler.runtime.build import test_command_for as resolve_test_command


def test_e2b_benchmark_passes_runtime_envs(monkeypatch) -> None:
    created: list[dict[str, object]] = []

    class Result:
        exit_code = 0

    class Commands:
        def run(self, command: str, *, user: str, timeout: int):
            assert command.startswith("env ")
            assert "PATH=" in command
            assert "timeout --signal=TERM --kill-after=10s 135s" in command
            assert user == "root"
            assert timeout == 165
            return Result()

    class Files:
        def read(self, path: str) -> str:
            assert path == "/tmp/time.log"
            return "Maximum resident set size (kbytes): 1024"

    class Sandbox:
        commands = Commands()
        files = Files()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        @classmethod
        def create(cls, **kwargs):
            created.append(kwargs)
            return cls()

    monkeypatch.setitem(sys.modules, "e2b", SimpleNamespace(Sandbox=Sandbox))
    envs = {"PATH": "/usr/local/go/bin:/usr/bin"}
    result = E2BBenchmark("test-key", runs=1).run(
        "repo-template",
        "go test ./...",
        envs=envs,
    )

    assert created[0]["allow_internet_access"] is False
    assert created[0]["envs"] == envs
    assert result.all_passed


def test_e2b_benchmark_runs_as_selected_user(monkeypatch) -> None:
    observed: dict[str, object] = {}

    class Result:
        exit_code = 0

    class Commands:
        def run(self, command: str, *, user: str, timeout: int):
            observed.update(command=command, user=user, timeout=timeout)
            return Result()

    class Files:
        def read(self, path: str) -> str:
            return "Maximum resident set size (kbytes): 1024"

    class Sandbox:
        commands = Commands()
        files = Files()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        @classmethod
        def create(cls, **kwargs):
            return cls()

    monkeypatch.setitem(sys.modules, "e2b", SimpleNamespace(Sandbox=Sandbox))
    result = E2BBenchmark("test-key", runs=1).run(
        "repo-template",
        "python -m pytest -q",
        envs={"HOME": "/home/user"},
        user="user",
    )

    assert result.all_passed
    assert observed["user"] == "user"
    assert "HOME=/home/user" in str(observed["command"])


def test_e2b_benchmark_stops_after_decisive_timeout(monkeypatch) -> None:
    created: list[dict[str, object]] = []

    class Result:
        exit_code = 124

    class Commands:
        def run(self, command: str, *, user: str, timeout: int):
            return Result()

    class Files:
        def read(self, path: str) -> str:
            return "Maximum resident set size (kbytes): 1024"

    class Sandbox:
        commands = Commands()
        files = Files()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        @classmethod
        def create(cls, **kwargs):
            created.append(kwargs)
            return cls()

    monkeypatch.setitem(sys.modules, "e2b", SimpleNamespace(Sandbox=Sandbox))
    result = E2BBenchmark("test-key", runs=3).run("repo-template", "pytest")

    assert len(created) == 1
    assert len(result.runs) == 1
    assert not result.all_passed


def test_parse_max_rss() -> None:
    log = "\tMaximum resident set size (kbytes): 262144\n"
    assert parse_max_rss(log) == 262_144
    assert parse_max_rss("missing") == -1


def test_summarize_runs_pass_and_flaky() -> None:
    runs = [
        BenchmarkRun(2.0, 10.0, 200.0, 0),
        BenchmarkRun(3.0, 11.0, 220.0, 0),
        BenchmarkRun(2.5, 12.0, 210.0, 0),
    ]
    result = summarize_runs(runs, "pytest")
    assert result.passed
    assert result.test_duration_median_s == 11.0

    runs[-1] = BenchmarkRun(2.5, 30.0, 210.0, 1)
    result = summarize_runs(runs, "pytest")
    assert result.flaky
    assert not result.passed


def test_subset_test_command(tmp_path) -> None:
    target = tmp_path / "pkg" / "codec"
    target.mkdir(parents=True)
    assert subset_test_command(tmp_path, "go", ["pkg/codec"]) == "go test ./pkg/codec/..."
    assert subset_test_command(tmp_path, "python", ["pkg/codec"]) == (
        "python -m pytest -x -q pkg/codec"
    )
    assert subset_test_command(tmp_path, "go", ["../escape"]) is None


def test_python_subset_maps_src_layout_to_test_directory(tmp_path) -> None:
    (tmp_path / "src" / "demo" / "config").mkdir(parents=True)
    (tmp_path / "tests" / "test_config").mkdir(parents=True)

    assert subset_test_command(tmp_path, "python", ["src/demo/config"]) == (
        "python -m pytest -x -q tests/test_config"
    )


def test_node_test_command_without_npm_test_script(tmp_path) -> None:
    (tmp_path / "package.json").write_text(
        '{"devDependencies":{"vitest":"2.0.0"}}', encoding="utf-8"
    )
    assert resolve_test_command("typescript", tmp_path) == "npx vitest run"


def test_dockerfile_uses_repository_runtime_version(tmp_path) -> None:
    (tmp_path / "go.mod").write_text("module example.com/demo\n\ngo 1.26.5\n", encoding="utf-8")
    dockerfile = dockerfile_for("go", tmp_path)
    assert dockerfile.startswith("FROM golang:1.22\n")
    assert "ENV GOTOOLCHAIN=auto\n" in dockerfile


def test_rust_dockerfile_ignores_versions_in_toolchain_comments(tmp_path) -> None:
    (tmp_path / "rust-toolchain.toml").write_text(
        '# Apache License, Version 2.0\n[toolchain]\nchannel = "stable"\n',
        encoding="utf-8",
    )
    (tmp_path / "Cargo.toml").write_text(
        '[package]\nname = "demo"\nversion = "0.1.0"\nrust-version = "1.90"\n',
        encoding="utf-8",
    )

    assert dockerfile_for("rust", tmp_path).startswith("FROM rust:1.90\n")
