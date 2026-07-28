from __future__ import annotations

from typing import Any, Protocol

from .harbor_packaging import HarborPackager
from .registry import JsonlRegistry
from .scoring import LanguageQuota


class PackageResult(Protocol):
    def to_dict(self) -> dict[str, Any]: ...


class CandidateRegistrar:
    """Build, package, and persist compact qualified candidate records."""

    def __init__(
        self,
        registry: JsonlRegistry,
        quota: LanguageQuota,
        packager: HarborPackager | None,
    ) -> None:
        self.registry = registry
        self.quota = quota
        self.packager = packager

    def register(
        self,
        repo: dict[str, Any],
        *,
        score: dict[str, Any],
        direction: dict[str, Any],
        build: dict[str, Any],
        environment: dict[str, Any] | None,
        template_id: str | None,
        benchmark: dict[str, Any] | None,
        adjusted_score: float,
        status: str,
    ) -> None:
        language = str(repo.get("language") or "").lower()
        record = {
            "repo": repo["full_name"],
            "base_commit": repo["base_commit"],
            "source_tree": repo.get("source_tree", ""),
            "default_branch": repo.get("default_branch") or "main",
            "license": (repo.get("license") or {}).get("spdx_id") or "NOASSERTION",
            "language": language,
            "stars": repo.get("stargazers_count", 0),
            "file_count": score["file_count"],
            "soft_score": score["total"],
            "adjusted_score": adjusted_score,
            "score": score,
            "test_cmd": build["test_cmd"],
            "local_image": build["image"],
            "local_image_retained": False,
            "e2b_template": template_id,
            "e2b_environment": compact_environment(environment),
            "benchmark": benchmark,
            "direction_source": direction["source"],
            "direction": direction["direction"],
            "direction_keywords": direction["keywords"],
            "direction_target_paths": direction["target_paths"],
            "h6_sources": direction.get("h6_sources", []),
            "status": status,
        }
        if self.packager is not None:
            package: PackageResult = self.packager.package(record)
            record["harbor_package"] = package.to_dict()
        self.registry.register(record)
        self.quota.register(language)


def compact_environment(environment: dict[str, Any] | None) -> dict[str, Any] | None:
    if environment is None:
        return None
    compact = dict(environment)
    offline = compact.get("offline")
    if offline:
        compact_offline = dict(offline)
        compact_offline.pop("stdout_tail", None)
        compact_offline.pop("stderr_tail", None)
        compact["offline"] = compact_offline
    return compact
