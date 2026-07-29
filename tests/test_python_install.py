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
        "/usr/local/bin/python -m pip install --no-cache-dir --upgrade 'pip>=25.1'",
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
        "/usr/local/bin/python -m pip install --no-cache-dir --upgrade 'pip>=25.1'",
        "/usr/local/bin/pip install --no-cache-dir pytest",
        "/usr/local/bin/pip install --no-cache-dir -e .",
    ]


def test_python_install_supports_pep735_and_poetry_groups(tmp_path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\n'
        '[dependency-groups]\ndev = ["nox"]\ntest = ["pytest-asyncio"]\n'
        '[tool.poetry.group.dev.dependencies]\nrespx = "^0.22"\n',
        encoding="utf-8",
    )

    assert python_install_commands(tmp_path) == [
        "/usr/local/bin/python -m pip install --no-cache-dir --upgrade 'pip>=25.1'",
        "/usr/local/bin/pip install --no-cache-dir pytest",
        "/usr/local/bin/pip install --no-cache-dir --group test",
        "/usr/local/bin/pip install --no-cache-dir --group dev",
        "/usr/local/bin/pip install --no-cache-dir poetry",
        "POETRY_VIRTUALENVS_CREATE=false /usr/local/bin/poetry install "
        "--no-interaction --no-root --with dev --all-extras",
        "/usr/local/bin/pip install --no-cache-dir -e .",
    ]
