from __future__ import annotations

from alvance_github_crawler.python_install import (
    declared_test_extras,
    python_install_commands,
)


def test_python_install_uses_only_declared_extras(tmp_path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\n'
        '[project.optional-dependencies]\ntest = ["pytest-asyncio"]\ndocs = ["mkdocs"]\n',
        encoding="utf-8",
    )
    (tmp_path / "requirements-dev.txt").write_text("ruff\n", encoding="utf-8")

    assert declared_test_extras(tmp_path / "pyproject.toml") == ("test",)
    assert python_install_commands(tmp_path) == [
        "/usr/local/bin/pip install --no-cache-dir pytest",
        "/usr/local/bin/pip install --no-cache-dir -r requirements-dev.txt",
        "/usr/local/bin/pip install --no-cache-dir -e '.[test]'",
    ]


def test_python_install_falls_back_to_plain_editable(tmp_path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\n',
        encoding="utf-8",
    )

    assert python_install_commands(tmp_path) == [
        "/usr/local/bin/pip install --no-cache-dir pytest",
        "/usr/local/bin/pip install --no-cache-dir -e .",
    ]
