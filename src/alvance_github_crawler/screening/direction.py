from __future__ import annotations

import json
import logging
import threading
import time
from typing import Any, Protocol

import requests
from openai import OpenAI
from pydantic import BaseModel, Field

from ..github import GitHubClient
from ..models import Direction

LOGGER = logging.getLogger(__name__)


class DirectionVerdict(BaseModel):
    implemented: bool
    behavior_boundary_clear: bool
    estimated_loc: int = Field(ge=0)
    keywords: list[str]
    direction: str
    target_paths: list[str] = Field(default_factory=list)


class Judge(Protocol):
    def judge(
        self, repo: dict[str, Any], issue: dict[str, Any], repo_tree_summary: str
    ) -> DirectionVerdict: ...


class OpenAIDirectionJudge:
    MAX_ATTEMPTS = 4
    RETRY_BASE_S = 5.0
    MIN_REQUEST_INTERVAL_S = 0.5

    SYSTEM_PROMPT = """你是代码库分析员。判断 issue 描述的功能是否已在仓库中实现。
只在行为边界清晰、预计实现至少 200 行、可以客观测试时推荐该方向。
keywords 应给出 2-5 个适合代码搜索、具有区分度的英文短语；target_paths 是可能受影响的路径。
direction 用一句中文准确概括待实现功能。
优先选择面向开发者的库类功能（如解析、序列化、协议、编解码、DSL、代码生成等），
拒绝选择面向终端用户的应用功能（如 UI 交互、业务流程、数据看板等）。"""

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str = "",
        *,
        timeout_s: int = 120,
        max_output_tokens: int = 1_000,
    ) -> None:
        # Shared retry coordination below handles overload without each worker
        # independently multiplying SDK retries.
        options = {"api_key": api_key, "timeout": timeout_s, "max_retries": 0}
        if base_url:
            options["base_url"] = base_url.rstrip("/")
        self.client = OpenAI(**options)
        self.model = model
        self.max_output_tokens = max_output_tokens
        self._request_lock = threading.Lock()
        self._next_request_at = 0.0

    def judge(
        self, repo: dict[str, Any], issue: dict[str, Any], repo_tree_summary: str
    ) -> DirectionVerdict:
        body = (issue.get("body") or "")[:6_000]
        user_input = (
            f"仓库: {repo['full_name']}\n"
            f"仓库描述: {repo.get('description') or ''}\n"
            f"仓库结构:\n{repo_tree_summary}\n\n"
            f"Issue #{issue['number']}: {issue.get('title') or ''}\n{body}"
        )
        response = None
        for attempt in range(self.MAX_ATTEMPTS):
            self._wait_for_request_window()
            try:
                response = self.client.responses.parse(
                    model=self.model,
                    instructions=self.SYSTEM_PROMPT,
                    input=user_input,
                    text_format=DirectionVerdict,
                    max_output_tokens=self.max_output_tokens,
                    reasoning={"effort": "low"},
                )
                break
            except Exception as exc:
                if attempt + 1 >= self.MAX_ATTEMPTS or not _is_retryable_openai_error(exc):
                    raise
                delay = _openai_retry_delay(exc, attempt, base_s=self.RETRY_BASE_S)
                self._defer_requests(delay)
                LOGGER.warning(
                    "direction judge retry repo=%s attempt=%d/%d delay_s=%.1f error=%s",
                    repo.get("full_name", "unknown"),
                    attempt + 1,
                    self.MAX_ATTEMPTS,
                    delay,
                    type(exc).__name__,
                )
        assert response is not None
        if response.output_parsed is None:
            raise RuntimeError("OpenAI response did not contain a parsed direction verdict")
        return response.output_parsed

    def _wait_for_request_window(self) -> None:
        with self._request_lock:
            now = time.monotonic()
            request_at = max(now, self._next_request_at)
            self._next_request_at = request_at + self.MIN_REQUEST_INTERVAL_S
        delay = request_at - now
        if delay > 0:
            time.sleep(delay)

    def _defer_requests(self, delay_s: float) -> None:
        with self._request_lock:
            self._next_request_at = max(
                self._next_request_at,
                time.monotonic() + delay_s,
            )


def _is_retryable_openai_error(error: BaseException) -> bool:
    status_code = getattr(error, "status_code", None)
    if status_code in {408, 409, 429, 500, 502, 503, 504}:
        return True
    return type(error).__name__ in {"APIConnectionError", "APITimeoutError"}


def _openai_retry_delay(error: BaseException, attempt: int, *, base_s: float) -> float:
    response = getattr(error, "response", None)
    headers = getattr(response, "headers", {}) or {}
    retry_after = headers.get("retry-after") or headers.get("Retry-After")
    try:
        if retry_after:
            return min(max(float(retry_after), 1.0), 60.0)
    except (TypeError, ValueError):
        pass

    body = getattr(error, "body", None)
    if isinstance(body, dict):
        retry_after = body.get("retry_after")
        if retry_after is None and isinstance(body.get("error"), dict):
            retry_after = body["error"].get("retry_after")
        try:
            if retry_after is not None:
                return min(max(float(retry_after), 1.0), 60.0)
        except (TypeError, ValueError):
            pass
    return min(base_s * (2**attempt), 60.0)


class PublicImplementationSearch:
    def __init__(self, github: GitHubClient, *, timeout: float = 30.0) -> None:
        self.github = github
        self.timeout = timeout
        self._last_grep_request = 0.0
        self._grep_lock = threading.Lock()
        self._thread_state = threading.local()

    @property
    def last_secondary_provider(self) -> str:
        return str(getattr(self._thread_state, "secondary_provider", "grep.app"))

    @last_secondary_provider.setter
    def last_secondary_provider(self, value: str) -> None:
        self._thread_state.secondary_provider = value

    def github_count(self, keywords: list[str]) -> int:
        return self.github.code_search_count(keywords)

    def grep_app_count(self, keywords: list[str]) -> int:
        with self._grep_lock:
            return self._grep_app_count(keywords)

    def _grep_app_count(self, keywords: list[str]) -> int:
        query = " ".join(keyword.strip() for keyword in keywords if keyword.strip())
        if not query:
            return 0
        for attempt in range(4):
            since_last = time.monotonic() - self._last_grep_request
            if since_last < 3.0:
                time.sleep(3.0 - since_last)
            try:
                response = requests.get(
                    "https://grep.app/api/search",
                    params={"q": query},
                    timeout=self.timeout,
                    headers={"User-Agent": "alvance-github-crawler/0.1"},
                )
            except requests.RequestException:
                self.last_secondary_provider = "sourcegraph_fallback"
                return self.sourcegraph_count(keywords)
            self._last_grep_request = time.monotonic()
            if response.headers.get("X-Vercel-Mitigated", "").lower() == "challenge":
                self.last_secondary_provider = "sourcegraph_fallback"
                return self.sourcegraph_count(keywords)
            if response.status_code != 429:
                response.raise_for_status()
                total = response.json().get("hits", {}).get("total", 0)
                self.last_secondary_provider = "grep.app"
                return int(total)
            retry_after = response.headers.get("Retry-After", "")
            try:
                delay = float(retry_after)
            except ValueError:
                delay = 5.0 * (2**attempt)
            time.sleep(min(max(delay, 3.0), 60.0))
        self.last_secondary_provider = "sourcegraph_fallback"
        return self.sourcegraph_count(keywords)

    def sourcegraph_count(self, keywords: list[str]) -> int:
        phrases = " ".join(
            f'"{keyword.replace(chr(34), "")}"' for keyword in keywords if keyword.strip()
        )
        query = f"context:global patternType:regexp {phrases} count:1 timeout:10s"
        response = requests.get(
            "https://sourcegraph.com/.api/search/stream",
            params={"q": query, "v": "V3"},
            stream=True,
            timeout=(10, 20),
            headers={"User-Agent": "alvance-github-crawler/0.1"},
        )
        response.raise_for_status()
        final_count = 0
        event = ""
        try:
            for raw_line in response.iter_lines(decode_unicode=True):
                if not raw_line:
                    continue
                if raw_line.startswith("event: "):
                    event = raw_line[7:].strip()
                    continue
                if not raw_line.startswith("data: "):
                    continue
                try:
                    payload = json.loads(raw_line[6:])
                except json.JSONDecodeError:
                    continue
                if event in {"error", "alert"}:
                    raise RuntimeError(
                        f"Sourcegraph search error: {payload!r}"
                    )
                if event == "matches" and isinstance(payload, list) and payload:
                    return 1
                if event == "progress" and isinstance(payload, dict):
                    final_count = max(final_count, int(payload.get("matchCount", 0) or 0))
                    if final_count > 0:
                        return final_count
        except requests.RequestException as exc:
            raise RuntimeError(f"Sourcegraph stream read error: {exc}") from exc
        return final_count


class DirectionChecker:
    def __init__(
        self,
        github: GitHubClient,
        judge: Judge,
        public_search: PublicImplementationSearch,
        *,
        issue_limit: int = 10,
    ) -> None:
        self.github = github
        self.judge = judge
        self.public_search = public_search
        self.issue_limit = issue_limit

    def check(self, repo: dict[str, Any], repo_tree_summary: str) -> Direction | None:
        issues = self.github.list_feature_issues(repo["full_name"], limit=self.issue_limit)
        for issue in issues:
            verdict = self.judge.judge(repo, issue, repo_tree_summary)
            if verdict.implemented or not verdict.behavior_boundary_clear:
                continue
            if verdict.estimated_loc < 200:
                continue
            keywords = [keyword.strip() for keyword in verdict.keywords if keyword.strip()][:5]
            if len(keywords) < 2:
                continue
            if self.public_search.github_count(keywords) > 0:
                continue
            if self.public_search.grep_app_count(keywords) > 0:
                continue
            return Direction(
                source=f"issue#{issue['number']}",
                direction=verdict.direction.strip(),
                keywords=keywords,
                target_paths=verdict.target_paths,
                h6_sources=[
                    "github_code_search",
                    getattr(self.public_search, "last_secondary_provider", "grep.app"),
                ],
            )
        return None
