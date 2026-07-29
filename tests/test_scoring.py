from __future__ import annotations

import json

from alvance_github_crawler.screening.scoring import (
    LanguageQuota,
    SoftScorer,
    count_public_symbols,
    is_developer_lib,
)


class FakeGitHub:
    def has_feature_issues(self, full_name: str) -> bool:
        return True


def test_language_quota_restores_registered_candidates(tmp_path) -> None:
    path = tmp_path / "candidates.jsonl"
    path.write_text(
        "\n".join(
            [
                json.dumps({"language": "go"}),
                json.dumps({"language": "python"}),
                json.dumps({"language": "python"}),
            ]
        ),
        encoding="utf-8",
    )
    quota = LanguageQuota(path)
    assert quota.counter["python"] == 2
    assert quota.quota_ok("typescript")
    assert not quota.quota_ok("python")


def test_developer_library_signals() -> None:
    assert is_developer_lib(
        {"name": "fast-parser", "description": "A protocol toolkit", "topics": ["library"]}
    )
    assert not is_developer_lib(
        {"name": "parser-dashboard", "description": "A parser web app", "topics": []}
    )


def test_public_symbol_count_and_complete_score(tmp_path) -> None:
    source = "\n".join(f"def public_{index}(): pass" for index in range(20))
    source += "\ndef _private(): pass\nclass PublicClass: pass\n"
    (tmp_path / "api.py").write_text(source, encoding="utf-8")
    assert count_public_symbols(tmp_path, "python") == 21

    repo = {
        "full_name": "owner/parser",
        "name": "parser",
        "description": "Protocol parsing library",
        "topics": ["sdk"],
        "language": "Python",
        "stargazers_count": 5_000,
    }
    tree = [{"type": "blob", "path": f"file-{index}"} for index in range(200)]
    score = SoftScorer(FakeGitHub(), LanguageQuota()).evaluate(repo, tree, tmp_path)
    assert score.file_count == 200
    assert score.public_symbol_count == 21
    assert score.details == {
        "S1_file_count": 2,
        "S2_stars": 2,
        "S3_feature_issues": 2,
        "S4_public_symbols": 2,
        "S5_language_quota": 0,
        "S6_developer_lib": 2,
    }
    assert score.total == 10
