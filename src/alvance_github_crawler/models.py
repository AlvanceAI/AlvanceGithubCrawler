from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class HardFilterResult:
    ok: bool
    reason: str


@dataclass(slots=True)
class ScoreResult:
    total: float
    file_count: int
    public_symbol_count: int
    quota_ok: bool
    developer_lib: bool
    details: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Direction:
    source: str
    direction: str
    keywords: list[str]
    target_paths: list[str] = field(default_factory=list)
    h6_sources: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class BuildResult:
    ok: bool
    reason: str
    image: str = ""
    dockerfile: str = ""
    test_cmd: str = ""
    log_tail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class BenchmarkRun:
    cold_start_s: float
    test_duration_s: float
    peak_mem_mb: float
    exit_code: int


@dataclass(slots=True)
class BenchmarkResult:
    runs: list[BenchmarkRun]
    cold_start_median_s: float
    test_duration_median_s: float
    peak_mem_median_mb: float
    all_passed: bool
    stable: bool
    resource_pass: bool
    passed: bool
    test_cmd: str

    @property
    def flaky(self) -> bool:
        return not self.stable

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
