from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from .github import GitHubClient
from .models import ScoreResult

LANG_QUOTA = {
    "go": 0.40,
    "python": 0.40,
    "typescript": 0.40,
    "javascript": 0.15,
    "rust": 0.15,
}

POSITIVE_LIB_SIGNALS = (
    "library",
    "sdk",
    "framework",
    "parser",
    "serializer",
    "client",
    "driver",
    "codec",
    "protocol",
    "compiler",
    "linter",
    "formatter",
    "middleware",
    "router",
    "orm",
    "rpc",
    "cli",
    "toolkit",
)

NEGATIVE_LIB_SIGNALS = (
    "app",
    "server",
    "dashboard",
    "website",
    "blog",
    "game",
    "bot",
    "scraper",
    "crawler",
    "monitor",
    "deploy",
)

SOURCE_EXTENSIONS = {
    "go": {".go"},
    "python": {".py"},
    "typescript": {".ts", ".tsx"},
    "javascript": {".js", ".jsx", ".mjs", ".cjs"},
    "rust": {".rs"},
}

PUBLIC_SYMBOL_PATTERNS = {
    "go": re.compile(r"^(?:func (?:\([^)]*\) )?[A-Z]\w*|type [A-Z]\w*)", re.MULTILINE),
    "python": re.compile(
        r"^(?:(?:async )?def [A-Za-z]\w*|class [A-Za-z]\w*)", re.MULTILINE
    ),
    "typescript": re.compile(r"^\s*export\s+(?:default\s+)?", re.MULTILINE),
    "javascript": re.compile(r"^\s*(?:export\s+|module\.exports\b)", re.MULTILINE),
    "rust": re.compile(
        r"^\s*pub(?:\([^)]*\))?\s+(?:async\s+)?(?:fn|struct|enum|trait)\s+",
        re.MULTILINE,
    ),
}


class LanguageQuota:
    def __init__(self, candidates_path: Path | None = None) -> None:
        self.counter: Counter[str] = Counter()
        if candidates_path and candidates_path.is_file():
            for line in candidates_path.read_text(encoding="utf-8").splitlines():
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                language = str(record.get("language", "")).lower()
                if language:
                    self.counter[language] += 1

    def quota_ok(self, language: str) -> bool:
        language = language.lower()
        projected_total = sum(self.counter.values()) + 1
        projected_language = self.counter[language] + 1
        return projected_language / projected_total <= LANG_QUOTA.get(language, 0.10)

    def register(self, language: str) -> None:
        self.counter[language.lower()] += 1


def is_developer_lib(repo: dict[str, Any]) -> bool:
    text = f"{repo.get('name', '')} {repo.get('description') or ''}".lower()
    topics = {str(topic).lower() for topic in repo.get("topics", [])}

    def contains(signal: str) -> bool:
        return signal in text or signal in topics

    positive = sum(1 for signal in POSITIVE_LIB_SIGNALS if contains(signal))
    negative = sum(1 for signal in NEGATIVE_LIB_SIGNALS if contains(signal))
    return positive > 0 and negative == 0


def count_public_symbols(repo_path: Path, language: str) -> int:
    pattern = PUBLIC_SYMBOL_PATTERNS.get(language)
    extensions = SOURCE_EXTENSIONS.get(language, set())
    if not pattern:
        return 0
    ignored = {".git", "node_modules", "vendor", "target", "dist", "build", ".venv"}
    count = 0
    for source in repo_path.rglob("*"):
        if not source.is_file() or source.suffix.lower() not in extensions:
            continue
        relative = source.relative_to(repo_path)
        if any(part in ignored for part in relative.parts):
            continue
        try:
            content = source.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        count += len(pattern.findall(content))
    return count


class SoftScorer:
    def __init__(self, github: GitHubClient, quota: LanguageQuota) -> None:
        self.github = github
        self.quota = quota

    def evaluate(
        self,
        repo: dict[str, Any],
        tree: list[dict[str, Any]],
        repo_path: Path,
    ) -> ScoreResult:
        language = (repo.get("language") or "").lower()
        file_count = sum(1 for item in tree if item.get("type") == "blob")
        symbol_count = count_public_symbols(repo_path, language)
        quota_ok = self.quota.quota_ok(language)
        developer_lib = is_developer_lib(repo)
        details: dict[str, float] = {}

        if 200 <= file_count <= 3_000:
            details["S1_file_count"] = 2
        elif 50 <= file_count < 200 or 3_000 < file_count <= 8_000:
            details["S1_file_count"] = 1
        else:
            details["S1_file_count"] = 0

        stars = int(repo.get("stargazers_count", 0))
        if 1_000 <= stars <= 50_000:
            details["S2_stars"] = 2
        elif stars >= 100:
            details["S2_stars"] = 1
        else:
            details["S2_stars"] = 0

        details["S3_feature_issues"] = 2 if self.github.has_feature_issues(repo["full_name"]) else 0
        details["S4_public_symbols"] = 2 if symbol_count >= 20 else 1
        details["S5_language_quota"] = 2 if quota_ok else 0
        details["S6_developer_lib"] = 2 if developer_lib else 0

        return ScoreResult(
            total=sum(details.values()),
            file_count=file_count,
            public_symbol_count=symbol_count,
            quota_ok=quota_ok,
            developer_lib=developer_lib,
            details=details,
        )

