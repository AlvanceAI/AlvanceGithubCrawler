from __future__ import annotations

from alvance_github_crawler.catalog.harbor_task import render_instruction, render_task_toml
from alvance_github_crawler.catalog.package_models import QualifiedRepository


def test_harbor_task_instruction_is_marked_as_direction_scaffold() -> None:
    repository = _repository()

    instruction = render_instruction(repository)
    manifest = render_task_toml(repository, "task-id", "material-id")

    assert instruction.startswith("# Direction scaffold")
    assert "not a locked DeepSWE instruction" in instruction
    assert 'status = "direction"' in manifest


def _repository() -> QualifiedRepository:
    return QualifiedRepository(
        repo="owner/project",
        base_commit="abcdef123456",
        source_tree="",
        default_branch="main",
        language="python",
        license="MIT",
        runtime_version="3.12",
        test_cmd="pytest",
        direction="Improve parser behavior.",
        source_template_alias="tmpl-source",
        dependency_commands=(),
        runtime_env={"PYTHONPATH": "/app"},
        execution_user="root",
    )
