from __future__ import annotations

import base64
import threading
import time
from typing import Any
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter


class GitHubError(RuntimeError):
    pass


class GitHubClient:
    api_url = "https://api.github.com"
    retryable_statuses = {403, 429, 500, 502, 503, 504}

    def __init__(
        self,
        token: str,
        *,
        timeout: float = 30.0,
        request_interval_s: float = 0.0,
        max_retries: int = 3,
        backoff_factor: float = 0.8,
        max_rate_limit_wait_s: float = 3_600.0,
    ) -> None:
        self.timeout = timeout
        self.request_interval_s = max(0.0, request_interval_s)
        self.max_retries = max(0, max_retries)
        self.backoff_factor = max(0.0, backoff_factor)
        self.max_rate_limit_wait_s = max(0.0, max_rate_limit_wait_s)
        self.request_count = 0
        self.retry_count = 0
        self.rate_limits: dict[str, dict[str, int | str]] = {}
        self._last_request_at = 0.0
        self._request_lock = threading.Lock()
        self.session = requests.Session()
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "alvance-github-crawler/0.1",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self.session.headers.update(headers)
        self.session.mount("https://", HTTPAdapter(max_retries=0))

    def _get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        allow_not_found: bool = False,
    ) -> requests.Response:
        return self._get_url(
            f"{self.api_url}{path}",
            params=params,
            allow_not_found=allow_not_found,
            error_path=path,
        )

    def _get_url(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        allow_not_found: bool = False,
        error_path: str | None = None,
    ) -> requests.Response:
        with self._request_lock:
            return self._get_url_serialized(
                url,
                params=params,
                allow_not_found=allow_not_found,
                error_path=error_path,
            )

    def _get_url_serialized(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        allow_not_found: bool = False,
        error_path: str | None = None,
    ) -> requests.Response:
        response: requests.Response | None = None
        last_error: requests.RequestException | None = None
        for attempt in range(self.max_retries + 1):
            self._pace_request()
            self.request_count += 1
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
                last_error = None
            except requests.RequestException as exc:
                last_error = exc
                if attempt >= self.max_retries:
                    break
                self.retry_count += 1
                time.sleep(self.backoff_factor * (2**attempt))
                continue

            self._record_rate_limit(response)
            if response.status_code not in self.retryable_statuses or attempt >= self.max_retries:
                break
            self.retry_count += 1
            time.sleep(self._retry_delay(response, attempt))

        display_path = error_path or url
        if response is None:
            message = f"GitHub request failed for {display_path}: {last_error}"
            raise GitHubError(message) from last_error
        if allow_not_found and response.status_code == 404:
            return response
        if response.status_code >= 400:
            remaining = response.headers.get("X-RateLimit-Remaining")
            reset = response.headers.get("X-RateLimit-Reset")
            detail = response.text[:500]
            raise GitHubError(
                f"GitHub API {response.status_code} for {display_path}; "
                f"remaining={remaining}, reset={reset}, response={detail}"
            )
        return response

    def _pace_request(self) -> None:
        if self.request_interval_s <= 0 or self._last_request_at <= 0:
            self._last_request_at = time.monotonic()
            return
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self.request_interval_s:
            time.sleep(self.request_interval_s - elapsed)
        self._last_request_at = time.monotonic()

    def _retry_delay(self, response: requests.Response, attempt: int) -> float:
        retry_after = response.headers.get("Retry-After", "")
        try:
            if retry_after:
                return min(max(0.0, float(retry_after)), self.max_rate_limit_wait_s)
        except ValueError:
            pass
        if response.headers.get("X-RateLimit-Remaining") == "0":
            reset = response.headers.get("X-RateLimit-Reset", "")
            try:
                delay = max(0.0, float(reset) - time.time()) + 1.0
                return min(delay, self.max_rate_limit_wait_s)
            except ValueError:
                pass
        return min(self.backoff_factor * (2**attempt), self.max_rate_limit_wait_s)

    def _record_rate_limit(self, response: requests.Response) -> None:
        resource = response.headers.get("X-RateLimit-Resource")
        if not resource:
            return
        values: dict[str, int | str] = {}
        for name, header in (
            ("limit", "X-RateLimit-Limit"),
            ("remaining", "X-RateLimit-Remaining"),
            ("used", "X-RateLimit-Used"),
            ("reset", "X-RateLimit-Reset"),
        ):
            raw_value = response.headers.get(header)
            if raw_value is None:
                continue
            try:
                values[name] = int(raw_value)
            except ValueError:
                values[name] = raw_value
        self.rate_limits[resource] = values

    def search_repositories_page(
        self, query: str, *, page: int = 1, per_page: int = 100
    ) -> dict[str, Any]:
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
        return dict(response.json())

    def search_repositories(
        self, query: str, *, pages: int = 1, per_page: int = 100
    ) -> list[dict[str, Any]]:
        repos: list[dict[str, Any]] = []
        page_size = min(per_page, 100)
        for page in range(1, pages + 1):
            items = self.search_repositories_page(
                query, page=page, per_page=page_size
            ).get("items", [])
            repos.extend(items)
            if len(items) < page_size:
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
            raw = self._get_url(download_url, error_path=f"raw content for {full_name}/{path}")
            return raw.text
        return None

    def get_head_commit(self, repo: dict[str, Any]) -> dict[str, str]:
        branch = str(repo.get("default_branch") or "")
        if not branch:
            raise GitHubError(f"default branch is missing for {repo.get('full_name', 'unknown')}")
        encoded_branch = quote(branch, safe="")
        response = self._get(f"/repos/{repo['full_name']}/commits/{encoded_branch}")
        payload = response.json()
        commit = payload.get("commit") or {}
        committer = commit.get("committer") or {}
        author = commit.get("author") or {}
        tree = commit.get("tree") or {}
        return {
            "sha": str(payload.get("sha") or ""),
            "tree_sha": str(tree.get("sha") or ""),
            "committed_at": str(committer.get("date") or author.get("date") or ""),
        }

    def get_head_sha(self, repo: dict[str, Any]) -> str:
        head = self.get_head_commit(repo)
        repo["source_tree"] = head["tree_sha"]
        return head["sha"]

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

    def get_rate_limit_status(self) -> dict[str, int]:
        response = self._get("/rate_limit")
        resources = response.json().get("resources") or {}
        remaining: dict[str, int] = {}
        for name, values in resources.items():
            if isinstance(values, dict) and isinstance(values.get("remaining"), int):
                remaining[str(name)] = int(values["remaining"])
        return remaining
