from __future__ import annotations

import json
import logging
import re
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from .github import GitHubClient
from .jsonl_io import append_text_locked, read_text_locked
from .screening.filters import PERMISSIVE_LICENSES, test_infrastructure_evidence
from .screening.scoring import developer_library_score

LOGGER = logging.getLogger(__name__)

CRAWL_LANGUAGES = ("python", "go", "typescript", "javascript", "rust")
GITHUB_LANGUAGE_NAMES = {
    "python": "Python",
    "go": "Go",
    "typescript": "TypeScript",
    "javascript": "JavaScript",
    "rust": "Rust",
}
CRAWL_STATE_VERSION = "1.1"
SELECTION_SEMANTICS = "raw_sample_all_pass_v1"
FULL_SHA = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)


class CrawlIncompleteError(RuntimeError):
    pass


class CandidateCrawler:
    def __init__(
        self,
        github: GitHubClient,
        output_dir: Path,
        *,
        target_total: int = 100,
        per_language: int = 20,
        max_search_pages: int = 10,
        now: datetime | None = None,
    ) -> None:
        expected_total = per_language * len(CRAWL_LANGUAGES)
        if per_language < 1:
            raise ValueError("per_language must be >= 1")
        if target_total != expected_total:
            raise ValueError(
                f"target_total must equal raw per_language * {len(CRAWL_LANGUAGES)} "
                f"({expected_total})"
            )
        if not 1 <= max_search_pages <= 10:
            raise ValueError("max_search_pages must be between 1 and 10")

        self.github = github
        self.output_dir = output_dir
        self.target_total = target_total
        self.per_language = per_language
        self.max_search_pages = max_search_pages
        self.now = now or datetime.now(UTC)
        if self.now.tzinfo is None:
            self.now = self.now.replace(tzinfo=UTC)
        self.cutoff = self.now - timedelta(days=365)

        self.raw_path = output_dir / "raw_repositories.jsonl"
        self.accepted_path = output_dir / "accepted_repositories.jsonl"
        self.rejected_path = output_dir / "rejected_repositories.jsonl"
        self.summary_path = output_dir / "summary.json"
        self.state_path = output_dir / "crawl_state.json"

        self.state: dict[str, Any] = {}
        self._prior_api_requests = 0
        self._prior_retries = 0

    def run(self) -> dict[str, Any]:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        raw_records = _read_jsonl(self.raw_path)
        accepted = _read_jsonl(self.accepted_path)
        rejected = _read_jsonl(self.rejected_path)
        self.state = self._load_state(raw_records)
        self._prior_api_requests = int(self.state.get("api_request_count", 0) or 0)
        self._prior_retries = int(self.state.get("retry_count", 0) or 0)

        errors = validate_accepted_records(accepted, cutoff=self.cutoff)
        if errors:
            raise CrawlIncompleteError("existing accepted output is invalid: " + "; ".join(errors))

        accepted_counts = Counter(str(item.get("language") or "").lower() for item in accepted)
        processed = {
            str(item.get("repo") or "").casefold()
            for item in [*accepted, *rejected]
            if item.get("repo")
        }
        if self._raw_sample_complete(raw_records) and len(processed) == self.target_total:
            previous_summary = _read_json(self.summary_path)
            if self._completed_summary_matches(previous_summary, raw_records, accepted, rejected):
                self._validate_completed(previous_summary)
                return previous_summary
            summary = self._write_summary(completed=True, refresh_rate_limit=False)
            self._validate_completed(summary)
            self._save_state(completed=True)
            return summary

        try:
            for language in CRAWL_LANGUAGES:
                while True:
                    pending = self._pending_for_language(raw_records, processed, language)
                    if pending:
                        self._process_pending(
                            pending,
                            language=language,
                            accepted=accepted,
                            rejected=rejected,
                            accepted_counts=accepted_counts,
                            processed=processed,
                        )
                        self._save_state(completed=False)

                    raw_count = self._raw_count(raw_records, language)
                    if raw_count >= self.per_language:
                        break

                    page = int(self.state["next_page_by_language"][language])
                    if page > self.max_search_pages:
                        raise CrawlIncompleteError(
                            f"{language} has only {raw_count} raw repositories "
                            f"after {self.max_search_pages} search pages"
                        )
                    items = self._fetch_page(language, page)
                    fetched_at = _utc_now()
                    page_records = []
                    known_raw = {
                        str(record.get("full_name") or "").casefold()
                        for record in raw_records
                        if record.get("full_name")
                    }
                    remaining = self.per_language - raw_count
                    for item in items:
                        if not isinstance(item, dict):
                            continue
                        key = str(item.get("full_name") or "").casefold()
                        if not key or key in known_raw:
                            continue
                        record = dict(item)
                        record["_crawl"] = {
                            "query_language": language,
                            "page": page,
                            "fetched_at": fetched_at,
                        }
                        page_records.append(record)
                        known_raw.add(key)
                        if len(page_records) >= remaining:
                            break
                    _append_jsonl_many(self.raw_path, page_records)
                    raw_records.extend(page_records)
                    self.state["next_page_by_language"][language] = page + 1
                    self._save_state(completed=False)
                    if not page_records:
                        raise CrawlIncompleteError(
                            f"GitHub search was exhausted for {language} at page {page}"
                        )
        except KeyboardInterrupt:
            self._save_state(completed=False)
            self._write_summary(completed=False, error="interrupted", refresh_rate_limit=False)
            raise
        except Exception as exc:
            self._save_state(completed=False)
            self._write_summary(
                completed=False,
                error=f"{type(exc).__name__}: {str(exc)[:500]}",
                refresh_rate_limit=False,
            )
            raise

        summary = self._write_summary(completed=True, refresh_rate_limit=True)
        self._validate_completed(summary)
        self._save_state(completed=True)
        return summary

    def _load_state(self, raw_records: list[dict[str, Any]]) -> dict[str, Any]:
        state = _read_json(self.state_path)
        if state:
            if state.get("selection_semantics") != SELECTION_SEMANTICS:
                raise CrawlIncompleteError(
                    "checkpoint uses the retired accepted-language-quota semantics; "
                    "choose a new output directory"
                )
            previous_target = int(state.get("target_total", 0))
            previous_per_language = int(state.get("per_language", 0))
            if self.target_total < previous_target or self.per_language < previous_per_language:
                raise CrawlIncompleteError("checkpoint sample size cannot be reduced")
            if self.target_total > previous_target or self.per_language > previous_per_language:
                state["target_total"] = self.target_total
                state["per_language"] = self.per_language
                state["completed"] = False
        else:
            state = {
                "schema_version": CRAWL_STATE_VERSION,
                "selection_semantics": SELECTION_SEMANTICS,
                "target_total": self.target_total,
                "per_language": self.per_language,
                "started_at": _utc_now(),
                "cutoff_time": self.cutoff.isoformat(),
                "next_page_by_language": {language: 1 for language in CRAWL_LANGUAGES},
                "api_request_count": 0,
                "retry_count": 0,
                "completed": False,
            }

        persisted_cutoff = _parse_github_time(str(state.get("cutoff_time") or ""))
        if persisted_cutoff is None:
            started_at = _parse_github_time(str(state.get("started_at") or "")) or self.now
            persisted_cutoff = started_at - timedelta(days=365)
            state["cutoff_time"] = persisted_cutoff.isoformat()
        self.cutoff = persisted_cutoff

        pages = state.setdefault(
            "next_page_by_language", {language: 1 for language in CRAWL_LANGUAGES}
        )
        for language in CRAWL_LANGUAGES:
            pages.setdefault(language, 1)
        for record in raw_records:
            crawl = record.get("_crawl") or {}
            language = str(crawl.get("query_language") or "").lower()
            page = int(crawl.get("page", 0) or 0)
            if language in CRAWL_LANGUAGES:
                pages[language] = max(int(pages[language]), page + 1)
        return state

    def _raw_count(self, raw_records: list[dict[str, Any]], language: str) -> int:
        return sum(
            1
            for record in raw_records
            if str((record.get("_crawl") or {}).get("query_language") or "").lower() == language
        )

    def _raw_sample_complete(self, raw_records: list[dict[str, Any]]) -> bool:
        return all(
            self._raw_count(raw_records, language) == self.per_language
            for language in CRAWL_LANGUAGES
        )

    def _pending_for_language(
        self,
        raw_records: list[dict[str, Any]],
        processed: set[str],
        language: str,
    ) -> list[dict[str, Any]]:
        unique: dict[str, dict[str, Any]] = {}
        for record in raw_records:
            crawl = record.get("_crawl") or {}
            query_language = str(crawl.get("query_language") or "").lower()
            repo_name = str(record.get("full_name") or "")
            key = repo_name.casefold()
            if query_language != language or not key or key in processed or key in unique:
                continue
            unique[key] = record
        return sorted(
            unique.values(),
            key=lambda repo: (
                -developer_library_score(repo),
                -int(repo.get("stargazers_count") or 0),
                str(repo.get("full_name") or "").casefold(),
            ),
        )

    def _process_pending(
        self,
        pending: list[dict[str, Any]],
        *,
        language: str,
        accepted: list[dict[str, Any]],
        rejected: list[dict[str, Any]],
        accepted_counts: Counter[str],
        processed: set[str],
    ) -> None:
        for repo in pending:
            repo_name = str(repo.get("full_name") or "")
            key = repo_name.casefold()
            if not key or key in processed:
                continue
            LOGGER.info("screening %s (%s)", repo_name, language)
            try:
                candidate, rejection = self._evaluate_repository(repo, language)
            except Exception as exc:
                candidate = None
                rejection = self._rejection(
                    repo,
                    language,
                    "inspection_error",
                    error_type=type(exc).__name__,
                    error=str(exc)[:1_000],
                )
            processed.add(key)
            if candidate is not None:
                _append_jsonl(self.accepted_path, candidate)
                accepted.append(candidate)
                accepted_counts[language] += 1
                LOGGER.info(
                    "accepted %s (%s accepted=%s)",
                    repo_name,
                    language,
                    accepted_counts[language],
                )
            else:
                assert rejection is not None
                _append_jsonl(self.rejected_path, rejection)
                rejected.append(rejection)

    def _evaluate_repository(
        self, repo: dict[str, Any], expected_language: str
    ) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
        reason = self._metadata_rejection(repo, expected_language)
        if reason:
            return None, self._rejection(repo, expected_language, reason)

        try:
            head = self.github.get_head_commit(repo)
        except Exception as exc:
            return None, self._rejection(
                repo,
                expected_language,
                "head_unavailable",
                error_type=type(exc).__name__,
                error=str(exc)[:1_000],
            )
        base_commit = str(head.get("sha") or "")
        if not FULL_SHA.fullmatch(base_commit):
            return None, self._rejection(repo, expected_language, "invalid_head_sha")
        committed_at = _parse_github_time(str(head.get("committed_at") or ""))
        if committed_at is None:
            return None, self._rejection(repo, expected_language, "missing_head_commit_time")
        if committed_at < self.cutoff:
            return None, self._rejection(repo, expected_language, "inactive_head_commit")

        try:
            tree = self.github.get_tree(str(repo["full_name"]), base_commit)
        except Exception as exc:
            return None, self._rejection(
                repo,
                expected_language,
                "tree_unavailable",
                error_type=type(exc).__name__,
                error=str(exc)[:1_000],
            )

        repo_for_filter = dict(repo)
        repo_for_filter["base_commit"] = base_commit
        try:
            evidence = test_infrastructure_evidence(
                self.github, repo_for_filter, expected_language, tree
            )
        except Exception as exc:
            return None, self._rejection(
                repo,
                expected_language,
                "test_inspection_error",
                error_type=type(exc).__name__,
                error=str(exc)[:1_000],
            )
        if not evidence:
            return None, self._rejection(repo, expected_language, "no_test_infra")

        license_info = repo.get("license") or {}
        source_tree = str(head.get("tree_sha") or "")
        candidate = {
            "repo": str(repo["full_name"]),
            "html_url": str(repo.get("html_url") or ""),
            "language": expected_language,
            "stars": int(repo.get("stargazers_count") or 0),
            "license": str(license_info.get("spdx_id") or ""),
            "description": repo.get("description"),
            "topics": [str(topic) for topic in (repo.get("topics") or [])],
            "default_branch": str(repo.get("default_branch") or ""),
            "base_commit": base_commit,
            "source_tree": source_tree,
            "head_commit_at": committed_at.isoformat(),
            "pushed_at": str(repo.get("pushed_at") or ""),
            "file_count": sum(1 for item in tree if item.get("type") == "blob"),
            "test_evidence": evidence,
            "developer_lib_score": developer_library_score(repo),
            "fork": False,
            "archived": False,
            "mirror": False,
            "crawl_time": _utc_now(),
        }
        return candidate, None

    def _metadata_rejection(self, repo: dict[str, Any], expected_language: str) -> str:
        if not repo.get("full_name"):
            return "invalid_repository_metadata"
        if int(repo.get("stargazers_count") or 0) < 100:
            return "stars_below_100"
        pushed_at = _parse_github_time(str(repo.get("pushed_at") or ""))
        if pushed_at is None or pushed_at < self.cutoff:
            return "inactive_push"
        license_info = repo.get("license") or {}
        if str(license_info.get("spdx_id") or "") not in PERMISSIVE_LICENSES:
            return "unsupported_license"
        if bool(repo.get("fork")):
            return "fork"
        if bool(repo.get("archived")):
            return "archived"
        if bool(repo.get("mirror_url")):
            return "mirror"
        if str(repo.get("language") or "").lower() != expected_language:
            return "language_mismatch"
        if not repo.get("default_branch"):
            return "missing_default_branch"
        return ""

    def _rejection(
        self,
        repo: dict[str, Any],
        language: str,
        reason: str,
        **details: Any,
    ) -> dict[str, Any]:
        return {
            "repo": str(repo.get("full_name") or "unknown"),
            "language": language,
            "reason": reason,
            "rejected_at": _utc_now(),
            **details,
        }

    def _fetch_page(self, language: str, page: int) -> list[dict[str, Any]]:
        query = (
            f"language:{GITHUB_LANGUAGE_NAMES[language]} stars:>=100 "
            f"pushed:>={self.cutoff.date().isoformat()} archived:false fork:false mirror:false"
        )
        LOGGER.info("fetching %s search page %s", language, page)
        payload = self.github.search_repositories_page(query, page=page, per_page=100)
        items = payload.get("items") or []
        if not isinstance(items, list):
            raise CrawlIncompleteError(f"GitHub search returned invalid items for {language}")
        return [item for item in items if isinstance(item, dict)]

    def _completed_summary_matches(
        self,
        summary: dict[str, Any],
        raw: list[dict[str, Any]],
        accepted: list[dict[str, Any]],
        rejected: list[dict[str, Any]],
    ) -> bool:
        return (
            self.state.get("completed") is True
            and summary.get("selection_semantics") == SELECTION_SEMANTICS
            and summary.get("status") == "completed"
            and summary.get("target_total") == self.target_total
            and summary.get("per_language") == self.per_language
            and summary.get("fetched_total") == len(raw)
            and summary.get("accepted_total") == len(accepted)
            and summary.get("rejected_total") == len(rejected)
        )

    def _save_state(self, *, completed: bool) -> None:
        self.state["api_request_count"] = self._prior_api_requests + self.github.request_count
        self.state["retry_count"] = self._prior_retries + self.github.retry_count
        self.state["completed"] = completed
        self.state["updated_at"] = _utc_now()
        _write_json_atomic(self.state_path, self.state)

    def _write_summary(
        self,
        *,
        completed: bool,
        error: str = "",
        refresh_rate_limit: bool,
    ) -> dict[str, Any]:
        previous_summary = _read_json(self.summary_path)
        rate_remaining: dict[str, int] = dict(
            previous_summary.get("github_rate_limit_remaining") or {}
        )
        if refresh_rate_limit:
            try:
                rate_remaining = self.github.get_rate_limit_status()
            except Exception as exc:
                LOGGER.warning("failed to refresh GitHub rate limit: %s", exc)
        if not rate_remaining:
            rate_remaining = {
                name: int(values["remaining"])
                for name, values in self.github.rate_limits.items()
                if isinstance(values.get("remaining"), int)
            }

        raw = _read_jsonl(self.raw_path)
        accepted = _read_jsonl(self.accepted_path)
        rejected = _read_jsonl(self.rejected_path)
        accepted_counts = Counter(str(item.get("language") or "").lower() for item in accepted)
        reasons = Counter(str(item.get("reason") or "unknown") for item in rejected)
        unique_raw = {
            str(item.get("full_name") or "").casefold() for item in raw if item.get("full_name")
        }
        ended_at = datetime.now(UTC)
        started_at = _parse_github_time(str(self.state.get("started_at") or "")) or ended_at
        validation_errors = validate_accepted_records(accepted, cutoff=self.cutoff)
        raw_counts = Counter(
            str((item.get("_crawl") or {}).get("query_language") or "").lower() for item in raw
        )
        if completed:
            if len(raw) != self.target_total:
                validation_errors.append(f"raw count is {len(raw)}, expected {self.target_total}")
            if len(unique_raw) != self.target_total:
                validation_errors.append(
                    f"unique raw count is {len(unique_raw)}, expected {self.target_total}"
                )
            for language in CRAWL_LANGUAGES:
                if raw_counts[language] != self.per_language:
                    validation_errors.append(
                        f"raw {language} count is {raw_counts[language]}, "
                        f"expected {self.per_language}"
                    )
            if len(accepted) + len(rejected) != self.target_total:
                validation_errors.append(
                    "accepted and rejected records do not cover the complete raw sample"
                )
        summary: dict[str, Any] = {
            "schema_version": CRAWL_STATE_VERSION,
            "selection_semantics": SELECTION_SEMANTICS,
            "status": "completed" if completed and not validation_errors else "incomplete",
            "target_total": self.target_total,
            "raw_per_language": self.per_language,
            "per_language": self.per_language,
            "cutoff_time": self.cutoff.isoformat(),
            "fetched_total": len(raw),
            "deduplicated_total": len(unique_raw),
            "duplicate_results": len(raw) - len(unique_raw),
            "accepted_total": len(accepted),
            "accepted_by_language": {
                language: accepted_counts[language] for language in CRAWL_LANGUAGES
            },
            "rejected_total": len(rejected),
            "rejected_by_reason": dict(sorted(reasons.items())),
            "api_request_count": self._prior_api_requests + self.github.request_count,
            "retry_count": self._prior_retries + self.github.retry_count,
            "github_rate_limit_remaining": rate_remaining,
            "search_pages_fetched": {
                language: int(self.state["next_page_by_language"][language]) - 1
                for language in CRAWL_LANGUAGES
            },
            "start_time": started_at.isoformat(),
            "end_time": ended_at.isoformat(),
            "duration_seconds": round((ended_at - started_at).total_seconds(), 3),
            "validation_errors": validation_errors,
            "output_dir": str(self.output_dir),
        }
        if error:
            summary["error"] = error
        _write_json_atomic(self.summary_path, summary)
        return summary

    def _validate_completed(self, summary: dict[str, Any]) -> None:
        errors = list(summary.get("validation_errors") or [])
        if errors:
            raise CrawlIncompleteError("crawl validation failed: " + "; ".join(errors))


def validate_accepted_records(
    records: list[dict[str, Any]],
    *,
    cutoff: datetime,
) -> list[str]:
    errors: list[str] = []
    repo_names = [str(item.get("repo") or "") for item in records]
    if len(set(name.casefold() for name in repo_names)) != len(repo_names):
        errors.append("accepted repositories contain duplicate names")
    for item in records:
        repo = str(item.get("repo") or "unknown")
        if not FULL_SHA.fullmatch(str(item.get("base_commit") or "")):
            errors.append(f"{repo}: invalid base_commit")
        if not item.get("default_branch"):
            errors.append(f"{repo}: missing default_branch")
        if not isinstance(item.get("test_evidence"), list) or not item["test_evidence"]:
            errors.append(f"{repo}: missing test_evidence")
        if int(item.get("stars") or 0) < 100:
            errors.append(f"{repo}: stars below 100")
        if str(item.get("license") or "") not in PERMISSIVE_LICENSES:
            errors.append(f"{repo}: unsupported license")
        if item.get("fork") or item.get("archived") or item.get("mirror"):
            errors.append(f"{repo}: fork, archived, or mirror flag is set")
        committed_at = _parse_github_time(str(item.get("head_commit_at") or ""))
        if committed_at is None or committed_at < cutoff:
            errors.append(f"{repo}: inactive or missing HEAD commit time")
    return errors


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    for line in read_text_locked(path).splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            records.append(value)
    return records


def _read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return dict(value) if isinstance(value, dict) else {}


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    _append_jsonl_many(path, [payload])


def _append_jsonl_many(path: Path, payloads: list[dict[str, Any]]) -> None:
    if not payloads:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = "".join(
        json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n" for payload in payloads
    )
    append_text_locked(path, serialized)


def _write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _parse_github_time(value: str) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.replace(tzinfo=UTC) if parsed.tzinfo is None else parsed.astimezone(UTC)


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()
