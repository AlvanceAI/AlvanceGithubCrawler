from __future__ import annotations

import json
from pathlib import Path

from ..github import GitHubClient
from ..jsonl_io import split_jsonl_lines
from .harbor_packaging import HarborPackager


def package_existing_candidates(
    candidates_path: Path,
    packager: HarborPackager,
    github: GitHubClient,
) -> dict[str, int]:
    stats = {"processed": 0, "packaged": 0, "error": 0}
    if not candidates_path.is_file():
        return stats
    for line in split_jsonl_lines(candidates_path.read_text(encoding="utf-8")):
        try:
            record = json.loads(line)
            stats["processed"] += 1
            enrich_candidate_record(record, github)
            packager.package(record)
            stats["packaged"] += 1
        except Exception:
            stats["error"] += 1
    return stats


def enrich_candidate_record(record: dict[str, object], github: GitHubClient) -> None:
    repo = str(record["repo"])
    commit = str(record["base_commit"])
    if not record.get("source_tree"):
        record["source_tree"] = github.get_commit_tree(repo, commit)
    if not record.get("default_branch") or not record.get("license"):
        metadata = github.get_repository(repo)
        if not record.get("default_branch"):
            record["default_branch"] = metadata.get("default_branch") or "main"
        if not record.get("license"):
            license_info = metadata.get("license") or {}
            record["license"] = license_info.get("spdx_id") or "NOASSERTION"
