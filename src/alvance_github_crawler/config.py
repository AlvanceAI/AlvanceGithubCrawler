from __future__ import annotations

import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

SUPPORTED_LANGUAGES = ("go", "python", "typescript", "javascript", "rust")
NUMBERED_E2B_KEY = re.compile(r"^E2B_API_KEY(\d+)$")
NUMBERED_GITHUB_TOKEN = re.compile(r"^GITHUB_TOKEN(\d+)$")


def parse_env_bool(value: str, *, default: bool = False) -> bool:
    if not value:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"invalid boolean environment value: {value}")


def dotenv_values(path: Path = Path(".env")) -> dict[str, str]:
    """Read a small, dependency-free subset of dotenv syntax without mutating env."""
    if not path.is_file():
        return {}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        values[key.strip()] = value
    return values


def load_dotenv(path: Path = Path(".env")) -> None:
    """Load dotenv values only when an actual environment value is absent."""
    for key, value in dotenv_values(path).items():
        os.environ.setdefault(key, value)


@dataclass(slots=True)
class PipelineConfig:
    github_token: str = ""
    github_tokens: tuple[str, ...] = field(default_factory=tuple)
    openai_api_key: str = ""
    openai_base_url: str = ""
    e2b_api_key: str = ""
    e2b_api_keys: tuple[str, ...] = field(default_factory=tuple)
    openai_model: str = "gpt-5-mini"
    output_dir: Path = Path(".crawler-state")
    catalog_dir: Path = Path("catalog")
    min_soft_score: float = 7.0
    max_candidates_per_query: int = 100
    search_pages: int = 1
    feature_issue_limit: int = 10
    openai_timeout_s: int = 120
    openai_max_output_tokens: int = 1_000
    build_timeout_s: int = 600
    benchmark_timeout_s: int = 600
    benchmark_runs: int = 3
    e2b_cpu_count: int = 1
    e2b_memory_mb: int = 1_024
    e2b_concurrency: int = 20
    prescreen_concurrency: int = 1
    language_quota_enabled: bool = False
    max_tree_entries: int = 1_500
    max_tree_chars: int = 18_000
    max_repo_size_kb: int = 100_000
    languages: tuple[str, ...] = field(default_factory=lambda: SUPPORTED_LANGUAGES)

    def __post_init__(self) -> None:
        github_tokens = tuple(dict.fromkeys(token for token in self.github_tokens if token))
        if not github_tokens and self.github_token:
            github_tokens = (self.github_token,)
        self.github_tokens = github_tokens
        if github_tokens:
            self.github_token = github_tokens[0]

        keys = tuple(dict.fromkeys(key for key in self.e2b_api_keys if key))
        if not keys and self.e2b_api_key:
            keys = (self.e2b_api_key,)
        self.e2b_api_keys = keys
        if keys:
            self.e2b_api_key = keys[0]

    @classmethod
    def from_env(cls) -> PipelineConfig:
        external_env = os.getenv("PIPELINE_ENV_FILE")
        # Process environment wins over files. An explicitly selected external file
        # then overrides the repository-local defaults for reproducible runs.
        sources = [dict(os.environ)]
        if external_env:
            sources.append(dotenv_values(Path(external_env).expanduser()))
        sources.append(dotenv_values())

        def value(*keys: str) -> str:
            for source in sources:
                for key in keys:
                    resolved = source.get(key, "")
                    if resolved:
                        return resolved
            return ""

        def e2b_keys() -> tuple[str, ...]:
            for source in sources:
                numbered_values: list[tuple[int, str]] = []
                for key, raw_value in source.items():
                    match = NUMBERED_E2B_KEY.fullmatch(str(key))
                    value = str(raw_value or "").strip()
                    if match and value:
                        numbered_values.append((int(match.group(1)), value))
                numbered = tuple(
                    dict.fromkeys(value for _, value in sorted(numbered_values))
                )
                if numbered:
                    return numbered
                fallback = str(source.get("E2B_API_KEY") or source.get("E2B_KEY") or "").strip()
                if fallback:
                    return (fallback,)
            return ()

        def github_tokens() -> tuple[str, ...]:
            for source in sources:
                numbered_values: list[tuple[int, str]] = []
                for key, raw_value in source.items():
                    match = NUMBERED_GITHUB_TOKEN.fullmatch(str(key))
                    token = str(raw_value or "").strip()
                    if match and token:
                        numbered_values.append((int(match.group(1)), token))
                numbered = tuple(
                    dict.fromkeys(token for _, token in sorted(numbered_values))
                )
                if numbered:
                    return numbered
                fallback = str(source.get("GITHUB_TOKEN") or "").strip()
                if fallback:
                    return (fallback,)
            fallback = discover_github_token()
            return (fallback,) if fallback else ()

        resolved_e2b_keys = e2b_keys()
        resolved_github_tokens = github_tokens()

        return cls(
            github_token=resolved_github_tokens[0] if resolved_github_tokens else "",
            github_tokens=resolved_github_tokens,
            openai_api_key=value("OPENAI_API_KEY", "MODEL_API_KEY"),
            openai_base_url=normalize_openai_base_url(value("OPENAI_BASE_URL", "MODEL_BASE_URL")),
            e2b_api_key=resolved_e2b_keys[0] if resolved_e2b_keys else "",
            e2b_api_keys=resolved_e2b_keys,
            openai_model=value("OPENAI_MODEL", "MODEL_NAME") or "gpt-5-mini",
            output_dir=Path(value("PIPELINE_OUTPUT_DIR") or ".crawler-state"),
            catalog_dir=Path(value("PIPELINE_CATALOG_DIR") or "catalog"),
            feature_issue_limit=int(value("PIPELINE_FEATURE_ISSUE_LIMIT") or "10"),
            openai_timeout_s=int(value("PIPELINE_OPENAI_TIMEOUT_S") or "120"),
            openai_max_output_tokens=int(value("PIPELINE_OPENAI_MAX_OUTPUT_TOKENS") or "1000"),
            e2b_cpu_count=int(value("PIPELINE_E2B_CPU_COUNT") or "1"),
            e2b_memory_mb=int(value("PIPELINE_E2B_MEMORY_MB") or "1024"),
            e2b_concurrency=int(value("PIPELINE_E2B_CONCURRENCY") or "20"),
            prescreen_concurrency=int(value("PIPELINE_PRESCREEN_CONCURRENCY") or "1"),
            language_quota_enabled=parse_env_bool(
                value("PIPELINE_LANGUAGE_QUOTA_ENABLED"), default=False
            ),
            max_repo_size_kb=int(value("PIPELINE_MAX_REPO_SIZE_KB") or "100000"),
        )

    def validate(self, *, require_e2b: bool = True) -> None:
        missing = []
        if not self.github_tokens:
            missing.append("GITHUB_TOKEN or GITHUB_TOKEN1/2")
        if not self.openai_api_key:
            missing.append("OPENAI_API_KEY")
        if require_e2b and not self.e2b_api_keys:
            missing.append("E2B_API_KEY or E2B_API_KEY1/2/3")
        if missing:
            raise ValueError(f"missing required environment variables: {', '.join(missing)}")
        if self.e2b_cpu_count < 1:
            raise ValueError("PIPELINE_E2B_CPU_COUNT must be >= 1")
        if self.e2b_memory_mb < 128:
            raise ValueError("PIPELINE_E2B_MEMORY_MB must be >= 128")
        if not 1 <= self.e2b_concurrency <= 20:
            raise ValueError("PIPELINE_E2B_CONCURRENCY must be between 1 and 20 per key")
        if not 1 <= self.prescreen_concurrency <= 20:
            raise ValueError("PIPELINE_PRESCREEN_CONCURRENCY must be between 1 and 20")

    @property
    def e2b_total_concurrency(self) -> int:
        return self.e2b_concurrency * max(1, len(self.e2b_api_keys))

    @property
    def queries(self) -> list[str]:
        cutoff = (datetime.now(UTC) - timedelta(days=365)).date().isoformat()
        return [
            f"language:{language} stars:100..200000 pushed:>{cutoff} "
            f"size:<{self.max_repo_size_kb} archived:false fork:false"
            for language in self.languages
        ]

    @property
    def candidates_path(self) -> Path:
        return self.output_dir / "candidates.jsonl"

    @property
    def rejections_path(self) -> Path:
        return self.output_dir / "rejections.jsonl"

    @property
    def pending_path(self) -> Path:
        return self.output_dir / "pending.jsonl"


def discover_github_token() -> str:
    """Reuse an existing GitHub CLI login without printing the credential."""
    if shutil.which("gh") is None:
        return ""
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def normalize_openai_base_url(value: str) -> str:
    value = value.strip().rstrip("/")
    if not value:
        return ""
    parsed = urlsplit(value)
    if parsed.path in {"", "/"}:
        parsed = parsed._replace(path="/v1")
    return urlunsplit(parsed).rstrip("/")
