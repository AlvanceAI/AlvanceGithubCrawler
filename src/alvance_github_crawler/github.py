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
        token: str | tuple[str, ...] | list[str],
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
        supplied_tokens = (token,) if isinstance(token, str) else tuple(token)
        self._tokens = tuple(
            dict.fromkeys(str(value).strip() for value in supplied_tokens if str(value).strip())
        )
        if not self._tokens:
            self._tokens = ("",)
        self._clients = tuple(
            _GitHubTokenClient(
                value,
                timeout=self.timeout,
                request_interval_s=self.request_interval_s,
                max_retries=self.max_retries,
                backoff_factor=self.backoff_factor,
                max_rate_limit_wait_s=self.max_rate_limit_wait_s,
            )
            for value in self._tokens
        )
        # Keep the legacy session attribute for callers/tests that customize a
        # single-token client. Multi-token requests use each lane's own session.
        self.session = self._clients[0].session
        self._selection_lock = threading.Lock()
        self._next_client_index = 0

    @property
    def token_count(self) -> int:
        return len(self._clients)

    @property
    def request_count(self) -> int:
        return sum(client.request_count for client in self._clients)

    @property
    def retry_count(self) -> int:
        return sum(client.retry_count for client in self._clients)

    @property
    def rate_limits(self) -> dict[str, dict[str, int | str]]:
        merged: dict[str, dict[str, int | str]] = {}
        for client in self._clients:
            for resource, values in client.rate_limits.items():
                current = merged.setdefault(resource, {})
                for name, value in values.items():
                    if name in {"limit", "remaining", "used"} and isinstance(value, int):
                        current[name] = int(current.get(name, 0) or 0) + value
                    elif name == "reset" and isinstance(value, int):
                        current[name] = max(int(current.get(name, 0) or 0), value)
                    else:
                        current.setdefault(name, value)
        return merged

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
        return self._next_client().get(
            url,
            params=params,
            allow_not_found=allow_not_found,
            error_path=error_path,
        )

    def _next_client(self) -> _GitHubTokenClient:
        with self._selection_lock:
            client = self._clients[self._next_client_index]
            self._next_client_index = (self._next_client_index + 1) % len(self._clients)
            return client

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
        remaining: dict[str, int] = {}
        errors: list[GitHubError] = []
        for client in self._clients:
            try:
                resources = client.get(
                    f"{self.api_url}/rate_limit", error_path="/rate_limit"
                ).json().get("resources") or {}
            except GitHubError as exc:
                errors.append(exc)
                continue
            for name, values in resources.items():
                if isinstance(values, dict) and isinstance(values.get("remaining"), int):
                    remaining[str(name)] = remaining.get(str(name), 0) + int(
                        values["remaining"]
                    )
        if not remaining and errors:
            raise errors[0]
        return remaining


class _GitHubTokenClient:
    """One independently rate-limited GitHub credential lane."""

    def __init__(
        self,
        token: str,
        *,
        timeout: float,
        request_interval_s: float,
        max_retries: int,
        backoff_factor: float,
        max_rate_limit_wait_s: float,
    ) -> None:
        self.timeout = timeout
        self.request_interval_s = request_interval_s
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.max_rate_limit_wait_s = max_rate_limit_wait_s
        self._request_count = 0
        self._retry_count = 0
        self._rate_limits: dict[str, dict[str, int | str]] = {}
        self._last_request_at = 0.0
        self._state_lock = threading.Lock()
        self._session_local = threading.local()
        self._headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "alvance-github-crawler/0.1",
        }
        if token:
            self._headers["Authorization"] = f"Bearer {token}"

    @property
    def session(self) -> requests.Session:
        session = getattr(self._session_local, "session", None)
        if session is None:
            session = requests.Session()
            session.headers.update(self._headers)
            session.mount(
                "https://",
                HTTPAdapter(pool_connections=20, pool_maxsize=20, max_retries=0),
            )
            self._session_local.session = session
        return session

    @property
    def request_count(self) -> int:
        with self._state_lock:
            return self._request_count

    @property
    def retry_count(self) -> int:
        with self._state_lock:
            return self._retry_count

    @property
    def rate_limits(self) -> dict[str, dict[str, int | str]]:
        with self._state_lock:
            return {resource: dict(values) for resource, values in self._rate_limits.items()}

    def get(
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
            with self._state_lock:
                self._request_count += 1
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
                last_error = None
            except requests.RequestException as exc:
                last_error = exc
                if attempt >= self.max_retries:
                    break
                with self._state_lock:
                    self._retry_count += 1
                time.sleep(self.backoff_factor * (2**attempt))
                continue

            self._record_rate_limit(response)
            if (
                response.status_code not in GitHubClient.retryable_statuses
                or attempt >= self.max_retries
            ):
                break
            with self._state_lock:
                self._retry_count += 1
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
        with self._state_lock:
            now = time.monotonic()
            request_at = max(now, self._last_request_at + self.request_interval_s)
            self._last_request_at = request_at
        delay = request_at - now
        if delay > 0:
            time.sleep(delay)

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
        with self._state_lock:
            self._rate_limits[resource] = values
