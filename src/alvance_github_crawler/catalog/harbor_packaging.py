from __future__ import annotations

import shlex
from pathlib import Path
from typing import Any

from ..e2b.wrapper import E2BHarborWrapperManager
from .package_models import (
    HarborPackageResult,
    QualifiedRepository,
    compact_package_record,
)
from .trace_store import TracePackageStore


class HarborPackager:
    """Orchestrate domain validation, E2B wrapping, and Trace persistence."""

    def __init__(
        self,
        api_key: str,
        catalog_dir: Path,
        *,
        cpu_count: int = 1,
        memory_mb: int = 1_024,
    ) -> None:
        self.wrapper_manager = E2BHarborWrapperManager(
            api_key,
            cpu_count=cpu_count,
            memory_mb=memory_mb,
        )
        self.store = TracePackageStore(catalog_dir)

    def package(self, candidate_record: dict[str, Any]) -> HarborPackageResult:
        repository = QualifiedRepository.from_candidate(candidate_record)
        prepared = self.store.prepare(repository)
        wrapper = self.wrapper_manager.ensure(
            repository,
            prepared.harbor_template_alias,
        )
        result = HarborPackageResult(
            package_id=prepared.material_id,
            material_id=prepared.material_id,
            task_name=prepared.task_name,
            material_path=prepared.material_path,
            task_path=prepared.task_path,
            source_template_alias=repository.source_template_alias,
            source_template_id=wrapper.source_template_id,
            harbor_template_alias=wrapper.harbor_template_alias,
            harbor_template_id=wrapper.harbor_template_id,
            wrapper_cache_hit=wrapper.cache_hit,
            wrapper_build_s=wrapper.build_duration_s,
            smoke_ok=bool(wrapper.smoke["ok"]),
            launch_command=(
                f"harbor run --path {shlex.quote(prepared.task_path)} --env e2b --no-force-build"
            ),
        )
        package_record = compact_package_record(
            candidate_record,
            repository,
            prepared,
            wrapper,
            result,
        )
        self.store.finalize(repository, prepared, wrapper, package_record)
        return result
