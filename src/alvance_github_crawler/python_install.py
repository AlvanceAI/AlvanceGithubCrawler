from __future__ import annotations

import shlex
import tomllib
from pathlib import Path

from .python_workspace import python_workspace_install_commands

PREFERRED_EXTRAS = (
    "test",
    "tests",
    "dev",
    "testing",
    "benchmark",
    "benchmarks",
    "benchmarking",
)
DYNAMIC_PREFERRED_EXTRAS = (*PREFERRED_EXTRAS, "optional", "all")
PREFERRED_GROUPS = PREFERRED_EXTRAS
REQUIREMENT_FILES = (
    "requirements-test.txt",
    "requirements-dev.txt",
    "requirements/tests.txt",
    "requirements/test.txt",
    "requirements/testing.txt",
    "requirements/dev.txt",
)


def python_install_commands(repo_path: Path) -> list[str]:
    """Build deterministic Python install steps from declared project metadata."""
    metadata = read_pyproject(repo_path / "pyproject.toml")
    groups = declared_dependency_groups(metadata)
    commands = []
    if groups:
        commands.append("/usr/local/bin/python -m pip install --no-cache-dir --upgrade 'pip>=25.1'")
    commands.append("/usr/local/bin/pip install --no-cache-dir pytest")
    requirements = [name for name in REQUIREMENT_FILES if (repo_path / name).is_file()]
    commands.extend(python_workspace_install_commands(repo_path, requirements))
    commands.extend(
        f"/usr/local/bin/pip install --no-cache-dir -r {shlex.quote(name)}" for name in requirements
    )
    commands.extend(
        f"/usr/local/bin/pip install --no-cache-dir --group {shlex.quote(group)}"
        for group in groups
    )
    if has_poetry_dev_group(metadata):
        commands.extend(
            [
                "/usr/local/bin/pip install --no-cache-dir poetry",
                "POETRY_VIRTUALENVS_CREATE=false /usr/local/bin/poetry install "
                "--no-interaction --no-root --with dev --all-extras",
            ]
        )
    extras = declared_test_extras(repo_path / "pyproject.toml")
    editable = f".[{','.join(extras)}]" if extras else "."
    commands.append(f"/usr/local/bin/pip install --no-cache-dir -e {shlex.quote(editable)}")
    return commands


def declared_test_extras(pyproject_path: Path) -> tuple[str, ...]:
    metadata = read_pyproject(pyproject_path)
    project = metadata.get("project") or {}
    if not isinstance(project, dict):
        return ()
    optional = project.get("optional-dependencies") or {}
    extras = [extra for extra in PREFERRED_EXTRAS if extra in optional]
    dynamic = project.get("dynamic") or []
    if "optional-dependencies" in dynamic:
        dynamic_optional = setuptools_dynamic_optional_dependencies(metadata)
        extras.extend(
            extra
            for extra in DYNAMIC_PREFERRED_EXTRAS
            if extra in dynamic_optional and extra not in extras
        )
    return tuple(extras)


def setuptools_dynamic_optional_dependencies(metadata: dict[str, object]) -> dict[str, object]:
    tool = metadata.get("tool") or {}
    if not isinstance(tool, dict):
        return {}
    setuptools = tool.get("setuptools") or {}
    if not isinstance(setuptools, dict):
        return {}
    dynamic = setuptools.get("dynamic") or {}
    if not isinstance(dynamic, dict):
        return {}
    optional = dynamic.get("optional-dependencies") or {}
    return optional if isinstance(optional, dict) else {}


def declared_dependency_groups(metadata: dict[str, object]) -> tuple[str, ...]:
    groups = metadata.get("dependency-groups") or {}
    if not isinstance(groups, dict):
        return ()
    return tuple(group for group in PREFERRED_GROUPS if group in groups)


def has_poetry_dev_group(metadata: dict[str, object]) -> bool:
    tool = metadata.get("tool") or {}
    if not isinstance(tool, dict):
        return False
    poetry = tool.get("poetry") or {}
    if not isinstance(poetry, dict):
        return False
    group = poetry.get("group") or {}
    return isinstance(group, dict) and "dev" in group


def read_pyproject(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {}
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError):
        return {}
