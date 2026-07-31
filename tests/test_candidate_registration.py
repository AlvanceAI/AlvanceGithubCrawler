from __future__ import annotations

import json

from alvance_github_crawler.pending.registration import CandidateRegistrar, compact_environment
from alvance_github_crawler.registry import JsonlRegistry
from alvance_github_crawler.screening.scoring import LanguageQuota


def test_compact_environment_removes_remote_test_logs() -> None:
    original = {
        "runtime_version": "1.26.5",
        "offline": {
            "ok": True,
            "duration_s": 4.2,
            "stdout_tail": "large stdout",
            "stderr_tail": "large stderr",
        },
    }

    compact = compact_environment(original)

    assert compact == {
        "runtime_version": "1.26.5",
        "offline": {"ok": True, "duration_s": 4.2},
    }
    assert "stdout_tail" in original["offline"]


def test_compact_environment_preserves_none() -> None:
    assert compact_environment(None) is None


def test_candidate_registration_persists_taskability_and_contamination(tmp_path) -> None:
    registry = JsonlRegistry(tmp_path / "candidates.jsonl", tmp_path / "rejections.jsonl")
    registrar = CandidateRegistrar(registry, LanguageQuota(), packager=None)

    registrar.register(
        {
            "full_name": "owner/project",
            "base_commit": "abcdef",
            "source_tree": "tree-sha",
            "default_branch": "main",
            "language": "Python",
            "description": "CLI parser and config toolkit",
            "topics": ["parser"],
            "license": {"spdx_id": "MIT"},
            "stargazers_count": 10,
        },
        score={"file_count": 12, "total": 8},
        direction={
            "source": "issue#123",
            "direction": "Improve config parser errors.",
            "keywords": ["config", "parser"],
            "target_paths": ["src/config.py"],
            "h6_sources": ["github_code_search"],
        },
        build={"test_cmd": "pytest", "image": "local-image"},
        environment={"offline": {"ok": True, "stdout_tail": "hidden"}},
        template_id="tmpl-1",
        benchmark={"test_duration_median_s": 30},
        adjusted_score=8.5,
        status="qualified",
    )

    record = json.loads(
        (tmp_path / "candidates.jsonl").read_text(encoding="utf-8").splitlines()[0]
    )
    assert record["taskability"]["score"] >= 3
    assert record["contamination"]["risk"] == "medium"
    assert record["e2b_environment"]["offline"] == {"ok": True}
