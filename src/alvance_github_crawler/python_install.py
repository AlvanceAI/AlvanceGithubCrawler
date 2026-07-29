from __future__ import annotations

import shlex
import tomllib
from pathlib import Path

PREFERRED_EXTRAS = ("test", "tests", "dev", "testing")
REQUIREMENT_FILES = (
    "requirements-test.txt",
    "requirements-dev.txt",
    "requirements/tests.txt",
    "requirements/test.txt",
    "requirements/dev.txt",
)


def python_install_commands(repo_path: Path) -> list[str]:
    """Build deterministic Python install steps from declared project metadata."""
    commands = ["/usr/local/bin/pip install --no-cache-dir pytest"]
    requirements = [name for name in REQUIREMENT_FILES if (repo_path / name).is_file()]
    commands.extend(
        f"/usr/local/bin/pip install --no-cache-dir -r {shlex.quote(name)}" for name in requirements
    )
    extras = declared_test_extras(repo_path / "pyproject.toml")
    editable = f".[{','.join(extras)}]" if extras else "."
    commands.append(f"/usr/local/bin/pip install --no-cache-dir -e {shlex.quote(editable)}")
    return commands


def declared_test_extras(pyproject_path: Path) -> tuple[str, ...]:
    if not pyproject_path.is_file():
        return ()
    try:
        with pyproject_path.open("rb") as handle:
            project = tomllib.load(handle).get("project") or {}
    except (OSError, tomllib.TOMLDecodeError):
        return ()
    optional = project.get("optional-dependencies") or {}
    return tuple(extra for extra in PREFERRED_EXTRAS if extra in optional)
