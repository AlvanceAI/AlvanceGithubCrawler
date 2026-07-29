from __future__ import annotations

import re
import shlex
from pathlib import Path

LOCAL_PACKAGE_PATTERN = re.compile(r"(?:^|\s)(?:-e\s+)?(?:\./)?(packages/[^\s;\[]+)")
NODE_BUILD_MARKERS = ("npm ", "npm\n", "node ", "node\n")


def python_workspace_install_commands(
    repo_path: Path,
    requirement_files: list[str],
) -> list[str]:
    """Install omitted local packages required by monorepo development environments."""
    omitted = omitted_workspace_packages(repo_path, requirement_files)
    if not omitted:
        return []

    commands: list[str] = []
    if any(package_requires_node(repo_path / path) for path in omitted):
        commands.append(
            "apt-get update && apt-get install -y --no-install-recommends nodejs npm "
            "&& rm -rf /var/lib/apt/lists/*"
        )
    commands.extend(
        f"/usr/local/bin/pip install --no-cache-dir -e {shlex.quote(path.as_posix())}"
        for path in omitted
    )
    return commands


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
