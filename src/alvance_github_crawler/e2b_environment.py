"""Compatibility exports for the split E2B environment modules."""

from .e2b_offline import E2BOfflineVerifier, OfflineTestResult
from .e2b_template_manager import (
    E2BEnvironmentManager,
    E2BEnvironmentResult,
    RepositoryTemplateBuildError,
    RuntimeTemplateBuildError,
)
from .e2b_template_manager import (
    _add_repository_build_steps as _add_repository_build_steps,
)
from .runtime_profiles import (
    command_with_environment,
    detect_runtime_version,
    hash_dependency_manifests,
    render_runtime_dockerfile,
    repository_template_alias,
    runtime_environment,
    runtime_template_alias,
)

__all__ = [
    "E2BEnvironmentManager",
    "E2BEnvironmentResult",
    "E2BOfflineVerifier",
    "OfflineTestResult",
    "RepositoryTemplateBuildError",
    "RuntimeTemplateBuildError",
    "command_with_environment",
    "detect_runtime_version",
    "hash_dependency_manifests",
    "render_runtime_dockerfile",
    "repository_template_alias",
    "runtime_environment",
    "runtime_template_alias",
]
