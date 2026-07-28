from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

SUPPORTED_LANGUAGES = ("go", "python", "typescript", "javascript", "rust")


def load_dotenv(path: Path = Path(".env")) -> None:
    """Load a small, dependency-free subset of dotenv syntax."""
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip("\"").strip("'")
        os.environ.setdefault(key.strip(), value)


@dataclass(slots=True)
class PipelineConfig:
    github_token: str = ""
    openai_api_key: str = ""
    openai_base_url: str = ""
    e2b_api_key: str = ""
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
    max_tree_entries: int = 1_500
    max_tree_chars: int = 18_000
    max_repo_size_kb: int = 100_000
    languages: tuple[str, ...] = field(default_factory=lambda: SUPPORTED_LANGUAGES)

    @classmethod
    def from_env(cls) -> PipelineConfig:
        external_env = os.getenv("PIPELINE_ENV_FILE")
        if external_env:
            load_dotenv(Path(external_env).expanduser())
        load_dotenv()
        return cls(
            github_token=os.getenv("GITHUB_TOKEN", "") or discover_github_token(),
            openai_api_key=os.getenv("OPENAI_API_KEY", "")
            or os.getenv("MODEL_API_KEY", ""),
            openai_base_url=normalize_openai_base_url(
                os.getenv("OPENAI_BASE_URL", "") or os.getenv("MODEL_BASE_URL", "")
            ),
            e2b_api_key=os.getenv("E2B_API_KEY", "") or os.getenv("E2B_KEY", ""),
            openai_model=os.getenv("OPENAI_MODEL", "")
            or os.getenv("MODEL_NAME", "")
            or "gpt-5-mini",
            output_dir=Path(os.getenv("PIPELINE_OUTPUT_DIR", ".crawler-state")),
            catalog_dir=Path(os.getenv("PIPELINE_CATALOG_DIR", "catalog")),
            feature_issue_limit=int(os.getenv("PIPELINE_FEATURE_ISSUE_LIMIT", "10")),
            openai_timeout_s=int(os.getenv("PIPELINE_OPENAI_TIMEOUT_S", "120")),
            openai_max_output_tokens=int(
                os.getenv("PIPELINE_OPENAI_MAX_OUTPUT_TOKENS", "1000")
            ),
            max_repo_size_kb=int(os.getenv("PIPELINE_MAX_REPO_SIZE_KB", "100000")),
        )

    def validate(self, *, require_e2b: bool = True) -> None:
        missing = []
        if not self.github_token:
            missing.append("GITHUB_TOKEN")
        if not self.openai_api_key:
            missing.append("OPENAI_API_KEY")
        if require_e2b and not self.e2b_api_key:
            missing.append("E2B_API_KEY")
        if missing:
            raise ValueError(f"missing required environment variables: {', '.join(missing)}")

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
