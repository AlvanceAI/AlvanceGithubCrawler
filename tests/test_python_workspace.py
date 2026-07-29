from __future__ import annotations

from alvance_github_crawler.runtime.python import (
    omitted_workspace_packages,
    python_workspace_install_commands,
    uv_workspace_packages,
)


def test_workspace_installs_omitted_local_package_and_node_toolchain(tmp_path) -> None:
    requirements = tmp_path / "requirements-dev.txt"
    requirements.write_text(
        "-e ./packages/server[all]\n-e ./packages/meta[all]\n",
        encoding="utf-8",
    )
    for name in ("server", "meta", "assets"):
        package = tmp_path / "packages" / name
        package.mkdir(parents=True)
        (package / "pyproject.toml").write_text(
            f'[project]\nname = "demo-{name}"\nversion = "1.0"\n',
            encoding="utf-8",
        )
    (tmp_path / "packages" / "assets" / "hatch_build.py").write_text(
        'subprocess.check_call("npm pack demo-assets")\n',
        encoding="utf-8",
    )

    assert omitted_workspace_packages(tmp_path, ["requirements-dev.txt"]) == (
        tmp_path.joinpath("packages/assets").relative_to(tmp_path),
    )
    assert python_workspace_install_commands(tmp_path, ["requirements-dev.txt"]) == [
        "apt-get update && apt-get install -y --no-install-recommends nodejs npm "
        "&& rm -rf /var/lib/apt/lists/*",
        "/usr/local/bin/pip install --no-cache-dir -e . -e packages/assets",
    ]


def test_workspace_is_inactive_without_local_requirement_references(tmp_path) -> None:
    package = tmp_path / "packages" / "unused"
    package.mkdir(parents=True)
    (package / "pyproject.toml").write_text(
        '[project]\nname = "unused"\nversion = "1.0"\n',
        encoding="utf-8",
    )
    (tmp_path / "requirements-dev.txt").write_text("pytest\n", encoding="utf-8")

    assert python_workspace_install_commands(tmp_path, ["requirements-dev.txt"]) == []


def test_workspace_installs_uv_members_before_dependency_groups(tmp_path) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[tool.uv.workspace]\nmembers = ["examples/*", "tests/fixtures/plugin"]\n',
        encoding="utf-8",
    )
    for relative in ("examples/parser", "tests/fixtures/plugin"):
        package = tmp_path / relative
        package.mkdir(parents=True)
        (package / "pyproject.toml").write_text(
            f'[project]\nname = "{package.name}"\nversion = "1.0"\n',
            encoding="utf-8",
        )

    expected = (
        tmp_path.joinpath("examples/parser").relative_to(tmp_path),
        tmp_path.joinpath("tests/fixtures/plugin").relative_to(tmp_path),
    )
    assert uv_workspace_packages(tmp_path) == expected
    assert python_workspace_install_commands(tmp_path, []) == [
        "/usr/local/bin/pip install --no-cache-dir -e . -e examples/parser "
        "-e tests/fixtures/plugin",
    ]
