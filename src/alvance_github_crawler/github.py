from __future__ import annotations

import base64
import time
from typing import Any
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class GitHubError(RuntimeError):
    pass


class GitHubClient:
    api_url = "https://api.github.com"

    def __init__(self, token: str, *, timeout: float = 30.0) -> None:
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "alvance-github-crawler/0.1",
            }
        )
        retry = Retry(
            total=3,
            backoff_factor=0.8,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET",),
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

    def _get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        allow_not_found: bool = False,
    ) -> requests.Response:
        response = self.session.get(f"{self.api_url}{path}", params=params, timeout=self.timeout)
        if response.status_code in {403, 429}:
            remaining = response.headers.get("X-RateLimit-Remaining")
            reset = response.headers.get("X-RateLimit-Reset")
            if remaining == "0" and reset:
                delay = max(0.0, float(reset) - time.time()) + 1.0
                if delay <= 65:
                    time.sleep(delay)
                    response = self.session.get(
                        f"{self.api_url}{path}", params=params, timeout=self.timeout
                    )
        if allow_not_found and response.status_code == 404:
            return response
        if response.status_code >= 400:
            remaining = response.headers.get("X-RateLimit-Remaining")
            reset = response.headers.get("X-RateLimit-Reset")
            detail = response.text[:500]
            raise GitHubError(
                f"GitHub API {response.status_code} for {path}; "
                f"remaining={remaining}, reset={reset}, response={detail}"
            )
        return response

    def search_repositories(
        self, query: str, *, pages: int = 1, per_page: int = 100
    ) -> list[dict[str, Any]]:
        repos: list[dict[str, Any]] = []
        for page in range(1, pages + 1):
            response = self._get(
                "/search/repositories",
                params={
                    "q": query,
                    "sort": "updated",
                    "order": "desc",
                    "per_page": min(per_page, 100),
                    "page": page,
                },
            )
            items = response.json().get("items", [])
            repos.extend(items)
            if len(items) < per_page:
                break
        return repos

    def get_tree(self, full_name: str, ref: str) -> list[dict[str, Any]]:
        encoded_ref = quote(ref, safe="")
        response = self._get(
            f"/repos/{full_name}/git/trees/{encoded_ref}", params={"recursive": "1"}
        )
        payload = response.json()
        if payload.get("truncated"):
            raise GitHubError(f"recursive tree for {full_name}@{ref} was truncated")
        return payload.get("tree", [])

    def get_file(self, full_name: str, path: str, *, ref: str | None = None) -> str | None:
        encoded_path = quote(path, safe="/")
        params = {"ref": ref} if ref else None
        response = self._get(
            f"/repos/{full_name}/contents/{encoded_path}",
            params=params,
            allow_not_found=True,
        )
        if response.status_code == 404:
            return None
        payload = response.json()
        content = payload.get("content")
        if content and payload.get("encoding") == "base64":
            return base64.b64decode(content).decode("utf-8", errors="replace")
        download_url = payload.get("download_url")
        if download_url:
            raw = self.session.get(download_url, timeout=self.timeout)
            raw.raise_for_status()
            return raw.text
        return None

    def get_head_sha(self, repo: dict[str, Any]) -> str:
        branch = repo.get("default_branch") or "HEAD"
        encoded_branch = quote(branch, safe="")
        response = self._get(f"/repos/{repo['full_name']}/commits/{encoded_branch}")
        payload = response.json()
        repo["source_tree"] = payload["commit"]["tree"]["sha"]
        return payload["sha"]

    def get_commit_tree(self, full_name: str, commit: str) -> str:
        response = self._get(f"/repos/{full_name}/git/commits/{quote(commit, safe='')}")
        return str(response.json()["tree"]["sha"])

    def get_repository(self, full_name: str) -> dict[str, Any]:
        response = self._get(f"/repos/{full_name}")
        return dict(response.json())

    def list_feature_issues(self, full_name: str, *, limit: int = 10) -> list[dict[str, Any]]:
        issues: dict[int, dict[str, Any]] = {}
        for label in ("enhancement", "feature", "roadmap"):
            response = self._get(
                f"/repos/{full_name}/issues",
                params={
                    "labels": label,
                    "state": "open",
                    # The /issues endpoint mixes issues and pull requests; fetch
                    # more than `limit` so PR filtering cannot empty the page.
                    "per_page": min(max(limit, 10), 100),
                },
            )
            for issue in response.json():
                if "pull_request" not in issue:
                    issues[issue["number"]] = issue
                if len(issues) >= limit:
                    break
            if len(issues) >= limit:
                break
        return list(issues.values())[:limit]

    def has_feature_issues(self, full_name: str) -> bool:
        return bool(self.list_feature_issues(full_name, limit=1))

    def code_search_count(self, keywords: list[str]) -> int:
        clean = [keyword.strip() for keyword in keywords if keyword.strip()][:5]
        if not clean:
            return 0
        query = " ".join(f'"{keyword.replace(chr(34), "")}"' for keyword in clean)
        response = self._get(
            "/search/code", params={"q": query, "per_page": 1}, allow_not_found=False
        )
        return int(response.json().get("total_count", 0))
