from __future__ import annotations

import re
import shlex
import tomllib
from pathlib import Path

LOCAL_PACKAGE_PATTERN = re.compile(r"(?:^|\s)(?:-e\s+)?(?:\./)?(packages/[^\s;\[]+)")
NODE_BUILD_MARKERS = ("npm ", "npm\n", "node ", "node\n")

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
CI_EXTRA_PATTERN = re.compile(r"\.\[([A-Za-z0-9_.\-,\s]+)\]")
CI_CONFIG_GLOBS = (
    ".github/workflows/*.yml",
    ".github/workflows/*.yaml",
    "tox.ini",
    "noxfile.py",
    "Makefile",
    "makefile",
    "justfile",
)

DEFAULT_COMMAND = "python -m pytest -x -q"
JUST_TEST_RECIPE = re.compile(r"^test(?:\s+[^:]*)?:\s*$")
JUST_TEMPLATE = re.compile(r"\{\{.*?\}\}")


# ---------------------------------------------------------------------------
# Workspace helpers (formerly python_workspace.py)
# ---------------------------------------------------------------------------


def python_workspace_install_commands(
    repo_path: Path,
    requirement_files: list[str],
) -> list[str]:
    """Install omitted local packages required by monorepo development environments."""
    packages = workspace_packages_to_install(repo_path, requirement_files)
    if not packages:
        return []

    commands: list[str] = []
    if any(package_requires_node(repo_path / path) for path in packages):
        commands.append(
            "apt-get update && apt-get install -y --no-install-recommends nodejs npm "
            "&& rm -rf /var/lib/apt/lists/*"
        )
    editable_paths = " ".join(
        f"-e {shlex.quote(path)}" for path in (".", *(item.as_posix() for item in packages))
    )
    commands.append(f"/usr/local/bin/pip install --no-cache-dir {editable_paths}")
    return commands


def workspace_packages_to_install(
    repo_path: Path,
    requirement_files: list[str],
) -> tuple[Path, ...]:
    packages = set(omitted_workspace_packages(repo_path, requirement_files))
    packages.update(uv_workspace_packages(repo_path))
    return tuple(sorted(packages, key=lambda path: path.as_posix()))


def omitted_workspace_packages(repo_path: Path, requirement_files: list[str]) -> tuple[Path, ...]:
    referenced = referenced_workspace_packages(repo_path, requirement_files)
    if not referenced:
        return ()
    available = {
        manifest.parent.relative_to(repo_path)
        for pattern in ("packages/*/pyproject.toml", "packages/*/setup.py")
        for manifest in repo_path.glob(pattern)
    }
    return tuple(sorted(available - referenced, key=lambda path: path.as_posix()))


def referenced_workspace_packages(repo_path: Path, requirement_files: list[str]) -> set[Path]:
    referenced: set[Path] = set()
    for name in requirement_files:
        try:
            content = (repo_path / name).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for line in content.splitlines():
            match = LOCAL_PACKAGE_PATTERN.search(line.split("#", 1)[0])
            if match:
                referenced.add(Path(match.group(1).rstrip("/")))
    return referenced


def uv_workspace_packages(repo_path: Path) -> tuple[Path, ...]:
    """Return installable local members declared by uv workspace metadata."""
    pyproject = repo_path / "pyproject.toml"
    try:
        with pyproject.open("rb") as handle:
            metadata = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError):
        return ()

    tool = metadata.get("tool") or {}
    uv = tool.get("uv") if isinstance(tool, dict) else None
    workspace = uv.get("workspace") if isinstance(uv, dict) else None
    members = workspace.get("members") if isinstance(workspace, dict) else None
    if not isinstance(members, list):
        return ()

    packages: set[Path] = set()
    for member in members:
        if not isinstance(member, str) or not member.strip():
            continue
        for path in repo_path.glob(member):
            if path.is_dir() and any(
                (path / manifest).is_file() for manifest in ("pyproject.toml", "setup.py")
            ):
                packages.add(path.relative_to(repo_path))
    return tuple(sorted(packages, key=lambda path: path.as_posix()))


def package_requires_node(package_path: Path) -> bool:
    for name in ("hatch_build.py", "setup.py", "pyproject.toml"):
        path = package_path / name
        try:
            content = path.read_text(encoding="utf-8", errors="replace").lower()
        except OSError:
            continue
        if any(marker in content for marker in NODE_BUILD_MARKERS):
            return True
    return (package_path / "package.json").is_file()


# ---------------------------------------------------------------------------
# Install commands (formerly python_install.py)
# ---------------------------------------------------------------------------


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
    if not isinstance(optional, dict):
        optional = {}
    extras = [extra for extra in PREFERRED_EXTRAS if extra in optional]
    dynamic = project.get("dynamic") or []
    if "optional-dependencies" in dynamic:
        dynamic_optional = setuptools_dynamic_optional_dependencies(metadata)
        extras.extend(
            extra
            for extra in DYNAMIC_PREFERRED_EXTRAS
            if extra in dynamic_optional and extra not in extras
        )
        optional = {**optional, **dynamic_optional}
    extras.extend(
        extra
        for extra in declared_ci_extras(pyproject_path.parent, set(optional))
        if extra not in extras
    )
    return tuple(extras)


def declared_ci_extras(repo_path: Path, available: set[str]) -> tuple[str, ...]:
    """Extract declared extras explicitly installed by upstream validation scripts."""
    selected: list[str] = []
    for pattern in CI_CONFIG_GLOBS:
        for path in sorted(repo_path.glob(pattern)):
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for match in CI_EXTRA_PATTERN.finditer(content):
                for raw_extra in match.group(1).split(","):
                    extra = raw_extra.strip()
                    if extra in available and extra not in selected:
                        selected.append(extra)
    return tuple(selected)


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


# ---------------------------------------------------------------------------
# Test command resolution (formerly python_test_command.py)
# ---------------------------------------------------------------------------


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
            .read_text(encoding="utf-8", errors="replace")
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
