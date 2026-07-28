from __future__ import annotations

from alvance_github_crawler.benchmark import parse_max_rss, subset_test_command, summarize_runs
from alvance_github_crawler.build import dockerfile_for
from alvance_github_crawler.build import test_command_for as resolve_test_command
from alvance_github_crawler.models import BenchmarkRun


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


def test_node_test_command_without_npm_test_script(tmp_path) -> None:
    (tmp_path / "package.json").write_text(
        '{"devDependencies":{"vitest":"2.0.0"}}', encoding="utf-8"
    )
    assert resolve_test_command("typescript", tmp_path) == "npx vitest run"


def test_dockerfile_uses_repository_runtime_version(tmp_path) -> None:
    (tmp_path / "go.mod").write_text("module example.com/demo\n\ngo 1.26.5\n", encoding="utf-8")
    assert dockerfile_for("go", tmp_path).startswith("FROM golang:1.26.5\n")
