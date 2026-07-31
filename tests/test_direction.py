from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace

import pytest

from alvance_github_crawler.screening.direction import (
    DirectionChecker,
    DirectionVerdict,
    OpenAIDirectionJudge,
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
        "alvance_github_crawler.screening.direction.requests.get",
        lambda *a, **k: ChallengeResponse(),
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


def test_grep_app_does_not_hold_rate_lock_during_network_request(monkeypatch) -> None:
    class SuccessResponse:
        status_code = 200
        headers: dict[str, str] = {}

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict[str, object]:
            return {"hits": {"total": 0}}

    barrier = threading.Barrier(2)

    def concurrent_response(*args, **kwargs):
        barrier.wait(timeout=1)
        return SuccessResponse()

    search = PublicImplementationSearch(FakeGitHub())
    search.GREP_REQUEST_INTERVAL_S = 0.0
    monkeypatch.setattr(
        "alvance_github_crawler.screening.direction.requests.get",
        concurrent_response,
    )

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(
            executor.map(
                search.grep_app_count,
                (["rare phrase", "one"], ["rare phrase", "two"]),
            )
        )

    assert results == [0, 0]


def test_openai_direction_judge_retries_shared_rate_limit(monkeypatch) -> None:
    verdict = DirectionVerdict(
        implemented=False,
        behavior_boundary_clear=True,
        estimated_loc=300,
        keywords=["binary frame", "stream checksum"],
        direction="增加流式帧校验",
    )

    class RateLimitError(RuntimeError):
        status_code = 429
        body = {"retry_after": 7}
        response = SimpleNamespace(headers={})

    class Responses:
        def __init__(self) -> None:
            self.calls = 0

        def parse(self, **kwargs):
            self.calls += 1
            if self.calls == 1:
                raise RateLimitError("retry later")
            return SimpleNamespace(output_parsed=verdict)

    judge = OpenAIDirectionJudge.__new__(OpenAIDirectionJudge)
    judge.client = SimpleNamespace(responses=Responses())
    judge.model = "test-model"
    judge.max_output_tokens = 100
    judge._request_lock = threading.Lock()
    judge._next_request_at = 0.0
    delays: list[float] = []
    monkeypatch.setattr(
        "alvance_github_crawler.screening.direction.time.monotonic",
        lambda: 0.0,
    )
    monkeypatch.setattr(
        "alvance_github_crawler.screening.direction.time.sleep",
        delays.append,
    )

    result = judge.judge(
        {"full_name": "owner/repo", "description": "test"},
        {"number": 1, "title": "feature", "body": "details"},
        "src/",
    )

    assert result == verdict
    assert judge.client.responses.calls == 2
    assert delays == [7.0]


def test_openai_direction_judge_does_not_retry_client_error(monkeypatch) -> None:
    class ClientError(RuntimeError):
        status_code = 400

    class Responses:
        def __init__(self) -> None:
            self.calls = 0

        def parse(self, **kwargs):
            self.calls += 1
            raise ClientError("invalid request")

    judge = OpenAIDirectionJudge.__new__(OpenAIDirectionJudge)
    judge.client = SimpleNamespace(responses=Responses())
    judge.model = "test-model"
    judge.max_output_tokens = 100
    judge._request_lock = threading.Lock()
    judge._next_request_at = 0.0
    monkeypatch.setattr(
        "alvance_github_crawler.screening.direction.time.monotonic",
        lambda: 0.0,
    )

    with pytest.raises(ClientError):
        judge.judge(
            {"full_name": "owner/repo", "description": "test"},
            {"number": 1, "title": "feature", "body": "details"},
            "src/",
        )

    assert judge.client.responses.calls == 1


def test_openai_direction_judge_falls_back_to_chat_completions() -> None:
    class NotFound(Exception):
        status_code = 404

    class FakeResponses:
        def __init__(self) -> None:
            self.calls = 0

        def parse(self, **kwargs):
            self.calls += 1
            raise NotFound("404 page not found")

    class FakeCompletions:
        def __init__(self) -> None:
            self.calls: list[dict[str, object]] = []

        def create(self, **kwargs):
            self.calls.append(kwargs)
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(
                            content=(
                                '{"implemented": false, '
                                '"behavior_boundary_clear": true, '
                                '"estimated_loc": 320, '
                                '"keywords": ["streaming checksum", "binary frame codec"], '
                                '"direction": "增加流式二进制帧编解码", '
                                '"target_paths": ["src/codec"]}'
                            )
                        )
                    )
                ]
            )

    responses = FakeResponses()
    completions = FakeCompletions()
    judge = OpenAIDirectionJudge.__new__(OpenAIDirectionJudge)
    judge.client = SimpleNamespace(
        responses=responses,
        chat=SimpleNamespace(completions=completions),
    )
    judge.model = "compatible-model"
    judge.max_output_tokens = 1000
    judge._request_lock = threading.Lock()
    judge._next_request_at = 0.0
    judge._responses_api_available = True

    verdict = judge.judge(
        {"full_name": "owner/repo", "description": ""},
        {"number": 1, "title": "feature", "body": "body"},
        "src/",
    )

    assert verdict.estimated_loc == 320
    assert verdict.target_paths == ["src/codec"]
    assert responses.calls == 1
    assert completions.calls[0]["response_format"] == {"type": "json_object"}
    assert judge._responses_api_available is False
