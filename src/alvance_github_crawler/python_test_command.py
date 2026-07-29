from __future__ import annotations

import re
import shlex
from pathlib import Path

DEFAULT_COMMAND = "python -m pytest -x -q"
JUST_TEST_RECIPE = re.compile(r"^test(?:\s+[^:]*)?:\s*$")
JUST_TEMPLATE = re.compile(r"\{\{.*?\}\}")


def python_test_command(repo_path: Path) -> str:
    """Resolve the narrowest upstream-declared pytest entry point."""
    target = justfile_pytest_target(repo_path)
    if target:
        return f"{DEFAULT_COMMAND} {target}"
    if has_explicit_pytest_collection_config(repo_path):
        return DEFAULT_COMMAND
    for name in ("tests", "test"):
        if (repo_path / name).is_dir():
            return f"{DEFAULT_COMMAND} {name}"
    return DEFAULT_COMMAND


def justfile_pytest_target(repo_path: Path) -> str:
    try:
        lines = (
            (repo_path / "justfile")
            .read_text(
                encoding="utf-8",
                errors="replace",
            )
            .splitlines()
        )
    except OSError:
        return ""

    in_test_recipe = False
    for line in lines:
        stripped = line.strip()
        if not in_test_recipe:
            if JUST_TEST_RECIPE.match(stripped):
                in_test_recipe = True
            continue
        if stripped and not line[0].isspace():
            if stripped.startswith("#"):
                continue
            break
        if "pytest" not in line:
            continue
        targets = pytest_targets_from_command(repo_path, line)
        if targets:
            return " ".join(shlex.quote(target) for target in targets)
    return ""


def pytest_targets_from_command(repo_path: Path, command: str) -> tuple[str, ...]:
    tail = JUST_TEMPLATE.sub("", command.split("pytest", 1)[1])
    try:
        tokens = shlex.split(tail)
    except ValueError:
        return ()

    targets: list[str] = []
    for token in tokens:
        if token.startswith("-") or token in {"&&", "||", ";", "|"}:
            continue
        path = Path(token)
        if path.is_absolute() or ".." in path.parts:
            continue
        if (repo_path / path).exists() and token not in targets:
            targets.append(token)
    return tuple(targets)


def has_explicit_pytest_collection_config(repo_path: Path) -> bool:
    if (repo_path / "pytest.ini").is_file():
        return True
    if "[tool.pytest.ini_options]" in _read(repo_path / "pyproject.toml"):
        return True
    for name in ("setup.cfg", "tox.ini"):
        content = _read(repo_path / name)
        if "[pytest]" in content or "[tool:pytest]" in content:
            return True
    return False


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
