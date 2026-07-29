from __future__ import annotations

import re
import shlex
import tomllib
from pathlib import Path

LOCAL_PACKAGE_PATTERN = re.compile(r"(?:^|\s)(?:-e\s+)?(?:\./)?(packages/[^\s;\[]+)")
NODE_BUILD_MARKERS = ("npm ", "npm\n", "node ", "node\n")


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
