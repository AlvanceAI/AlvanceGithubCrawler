from __future__ import annotations

from alvance_github_crawler.e2b_environment import (
    detect_runtime_version,
    hash_dependency_manifests,
    render_runtime_dockerfile,
    repository_template_alias,
    runtime_template_alias,
)


def test_go_runtime_and_template_recipe(tmp_path) -> None:
    (tmp_path / "go.mod").write_text(
        "module example.com/demo\n\ngo 1.26.5\n", encoding="utf-8"
    )
    version = detect_runtime_version("go", tmp_path)
    assert version == "1.26.5"
    dockerfile = render_runtime_dockerfile("go", version)
    assert "GOTOOLCHAIN=go1.26.5+auto" in dockerfile
    assert "PATH=/usr/local/go/bin" in dockerfile
    assert runtime_template_alias("go", version) == (
        "alvance-runtime-go-1-26-5-amd64-v3"
    )


def test_dependency_hash_changes_with_lockfile(tmp_path) -> None:
    (tmp_path / "package.json").write_text('{"name":"demo"}', encoding="utf-8")
    first = hash_dependency_manifests("typescript", tmp_path)
    (tmp_path / "package-lock.json").write_text("{}", encoding="utf-8")
    second = hash_dependency_manifests("typescript", tmp_path)
    assert first != second


def test_repository_alias_is_bounded() -> None:
    alias = repository_template_alias(
        "organization-with-a-very-long-name/repository-with-a-very-long-name",
        "a" * 40,
        "b" * 16,
    )
    assert len(alias) <= 63
