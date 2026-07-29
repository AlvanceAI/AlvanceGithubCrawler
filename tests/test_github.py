from __future__ import annotations

from typing import Any

from alvance_github_crawler.github import GitHubClient


class FakeResponse:
    def __init__(
        self,
        status_code: int,
        payload: dict[str, Any],
        *,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.status_code = status_code
        self._payload = payload
        self.headers = headers or {}
        self.text = str(payload)

    def json(self) -> dict[str, Any]:
        return self._payload


def test_github_client_retries_and_tracks_rate_limit(monkeypatch) -> None:
    client = GitHubClient("token", max_retries=2, backoff_factor=0)
    responses = iter(
        [
            FakeResponse(500, {"message": "temporary"}),
            FakeResponse(
                200,
                {"items": [{"full_name": "owner/repo"}]},
                headers={
                    "X-RateLimit-Resource": "search",
                    "X-RateLimit-Limit": "30",
                    "X-RateLimit-Remaining": "29",
                },
            ),
        ]
    )
    monkeypatch.setattr(client.session, "get", lambda *args, **kwargs: next(responses))

    payload = client.search_repositories_page("language:python", page=1)

    assert payload["items"][0]["full_name"] == "owner/repo"
    assert client.request_count == 2
    assert client.retry_count == 1
    assert client.rate_limits["search"]["remaining"] == 29


def test_github_client_retries_rate_and_server_statuses(monkeypatch) -> None:
    for retry_status in (403, 429, 503):
        client = GitHubClient("token", max_retries=1, backoff_factor=0)
        responses = iter(
            [
                FakeResponse(retry_status, {"message": "retry"}, headers={"Retry-After": "0"}),
                FakeResponse(200, {"items": []}),
            ]
        )
        monkeypatch.setattr(
            client.session,
            "get",
            lambda *args, _responses=responses, **kwargs: next(_responses),
        )

        assert client.search_repositories_page("language:python")["items"] == []
        assert client.retry_count == 1


def test_get_head_commit_returns_commit_and_tree(monkeypatch) -> None:
    client = GitHubClient("token", max_retries=0)
    response = FakeResponse(
        200,
        {
            "sha": "a" * 40,
            "commit": {
                "tree": {"sha": "b" * 40},
                "committer": {"date": "2026-07-01T00:00:00Z"},
            },
        },
    )
    monkeypatch.setattr(client.session, "get", lambda *args, **kwargs: response)

    head = client.get_head_commit({"full_name": "owner/repo", "default_branch": "main"})

    assert head == {
        "sha": "a" * 40,
        "tree_sha": "b" * 40,
        "committed_at": "2026-07-01T00:00:00Z",
    }
