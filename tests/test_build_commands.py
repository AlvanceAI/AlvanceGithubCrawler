from __future__ import annotations

from alvance_github_crawler.build import test_command_for as resolve_test_command


def test_python_command_targets_conventional_tests_directory(tmp_path) -> None:
    (tmp_path / "tests").mkdir()
    (tmp_path / "examples").mkdir()

    assert resolve_test_command("python", tmp_path) == "python -m pytest -x -q tests"


def test_python_command_supports_singular_test_directory(tmp_path) -> None:
    (tmp_path / "test").mkdir()

    assert resolve_test_command("python", tmp_path) == "python -m pytest -x -q test"


def test_python_command_respects_explicit_pytest_collection_config(tmp_path) -> None:
    (tmp_path / "tests").mkdir()
    (tmp_path / "pyproject.toml").write_text(
        '[tool.pytest.ini_options]\ntestpaths = ["checks"]\n',
        encoding="utf-8",
    )

    assert resolve_test_command("python", tmp_path) == "python -m pytest -x -q"


def test_python_command_prefers_upstream_justfile_test_target(tmp_path) -> None:
    (tmp_path / "tests" / "functional").mkdir(parents=True)
    (tmp_path / "tests" / "perf").mkdir()
    (tmp_path / "justfile").write_text(
        'test flags="":\n'
        "\tuv run --group test pytest {{ flags }} tests/functional\n\n"
        "coverage:\n"
        "\tuv run coverage run -m pytest tests\n",
        encoding="utf-8",
    )

    assert resolve_test_command("python", tmp_path) == "python -m pytest -x -q tests/functional"
