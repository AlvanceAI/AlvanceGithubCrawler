from __future__ import annotations

from alvance_github_crawler.screening.direction import (
    DirectionChecker,
    DirectionVerdict,
    PublicImplementationSearch,
)


class FakeGitHub:
    def list_feature_issues(self, full_name: str, *, limit: int):
        return [
            {"number": 1, "title": "small", "body": "x"},
            {"number": 2, "title": "candidate", "body": "y"},
        ]


class FakeJudge:
    def judge(self, repo, issue, repo_tree_summary):
        if issue["number"] == 1:
            return DirectionVerdict(
                implemented=False,
                behavior_boundary_clear=True,
                estimated_loc=50,
                keywords=["small feature", "tiny hook"],
                direction="太小",
            )
        return DirectionVerdict(
            implemented=False,
            behavior_boundary_clear=True,
            estimated_loc=350,
            keywords=["binary frame codec", "streaming checksum"],
            direction="增加流式二进制帧编解码",
            target_paths=["src/codec"],
        )


class FakeSearch:
    def github_count(self, keywords):
        return 0

    def grep_app_count(self, keywords):
        return 0


def test_direction_checker_skips_shallow_issue() -> None:
    checker = DirectionChecker(FakeGitHub(), FakeJudge(), FakeSearch())
    direction = checker.check({"full_name": "owner/repo"}, "src/\n")
    assert direction is not None
    assert direction.source == "issue#2"
    assert direction.target_paths == ["src/codec"]


def test_direction_checker_enforces_public_search() -> None:
    class SearchWithHit(FakeSearch):
        def github_count(self, keywords):
            return 1

    checker = DirectionChecker(FakeGitHub(), FakeJudge(), SearchWithHit())
    assert checker.check({"full_name": "owner/repo"}, "src/\n") is None


def test_grep_app_challenge_uses_sourcegraph(monkeypatch) -> None:
    class ChallengeResponse:
        status_code = 429
        headers = {"X-Vercel-Mitigated": "challenge"}

    search = PublicImplementationSearch(FakeGitHub())
    monkeypatch.setattr(
        "alvance_github_crawler.screening.direction.requests.get", lambda *a, **k: ChallengeResponse()
    )
    monkeypatch.setattr(search, "sourcegraph_count", lambda keywords: 0)
    assert search.grep_app_count(["rare phrase", "another phrase"]) == 0
    assert search.last_secondary_provider == "sourcegraph_fallback"


def test_grep_app_timeout_uses_sourcegraph(monkeypatch) -> None:
    search = PublicImplementationSearch(FakeGitHub())

    def timeout(*args, **kwargs):
        import requests

        raise requests.Timeout("unavailable")

    monkeypatch.setattr("alvance_github_crawler.screening.direction.requests.get", timeout)
    monkeypatch.setattr(search, "sourcegraph_count", lambda keywords: 0)
    assert search.grep_app_count(["rare phrase", "another phrase"]) == 0
    assert search.last_secondary_provider == "sourcegraph_fallback"
