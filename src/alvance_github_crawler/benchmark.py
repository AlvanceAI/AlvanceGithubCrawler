from __future__ import annotations

import re
import shlex
import statistics
import time
from pathlib import Path

from .models import BenchmarkResult, BenchmarkRun
from .runtime_profiles import command_with_environment

THRESHOLDS = {
    "cold_start_s": 20.0,
    "test_duration_s": 120.0,
    "peak_mem_mb": 4_096.0,
}


def parse_max_rss(log: str) -> int:
    for line in log.splitlines():
        if "Maximum resident set size" in line:
            match = re.search(r":\s*(\d+)\s*$", line)
            if match:
                return int(match.group(1))
    return -1


def summarize_runs(runs: list[BenchmarkRun], test_cmd: str) -> BenchmarkResult:
    if not runs:
        raise ValueError("at least one benchmark run is required")
    cold_starts = [run.cold_start_s for run in runs]
    durations = [run.test_duration_s for run in runs]
    memories = [run.peak_mem_mb for run in runs]
    exit_codes = [run.exit_code for run in runs]
    cold_median = round(float(statistics.median(cold_starts)), 2)
    duration_median = round(float(statistics.median(durations)), 2)
    memory_median = round(float(statistics.median(memories)), 1)
    all_passed = all(code == 0 for code in exit_codes)
    stable = max(durations) - min(durations) < 15 and len(set(exit_codes)) == 1
    resource_pass = (
        cold_median < THRESHOLDS["cold_start_s"]
        and duration_median < THRESHOLDS["test_duration_s"]
        and 0 <= memory_median < THRESHOLDS["peak_mem_mb"]
    )
    return BenchmarkResult(
        runs=runs,
        cold_start_median_s=cold_median,
        test_duration_median_s=duration_median,
        peak_mem_median_mb=memory_median,
        all_passed=all_passed,
        stable=stable,
        resource_pass=resource_pass,
        passed=all_passed and stable and resource_pass,
        test_cmd=test_cmd,
    )


class E2BTemplateBuilder:
    def __init__(self, api_key: str, *, cpu_count: int = 2, memory_mb: int = 4_096) -> None:
        self.api_key = api_key
        self.cpu_count = cpu_count
        self.memory_mb = memory_mb

    def build(self, repo_path: Path, dockerfile: str, alias: str) -> str:
        try:
            from e2b import Template
        except ImportError as exc:
            raise RuntimeError("e2b SDK is not installed; install the project with [e2b]") from exc

        if Template.alias_exists(alias, api_key=self.api_key):
            return alias
        template = Template(file_context_path=repo_path).from_dockerfile(dockerfile)
        info = Template.build(
            template,
            name=alias,
            alias=alias,
            cpu_count=self.cpu_count,
            memory_mb=self.memory_mb,
            api_key=self.api_key,
        )
        return info.template_id


class E2BBenchmark:
    def __init__(
        self,
        api_key: str,
        *,
        runs: int = 3,
        command_timeout_s: int = 600,
    ) -> None:
        self.api_key = api_key
        self.runs = runs
        self.command_timeout_s = command_timeout_s

    def run(
        self,
        template_id: str,
        test_cmd: str,
        *,
        envs: dict[str, str] | None = None,
    ) -> BenchmarkResult:
        try:
            from e2b import Sandbox
        except ImportError as exc:
            raise RuntimeError("e2b SDK is not installed; install the project with [e2b]") from exc

        runs: list[BenchmarkRun] = []
        timed_command = f"/usr/bin/time -v -o /tmp/time.log sh -c {shlex.quote(test_cmd)}"
        sandbox_command = command_with_environment(timed_command, envs)
        for _ in range(self.runs):
            started = time.monotonic()
            try:
                sandbox = Sandbox.create(
                    template=template_id,
                    allow_internet_access=False,
                    timeout=self.command_timeout_s + 60,
                    envs=envs,
                    api_key=self.api_key,
                )
                cold_start = time.monotonic() - started
                with sandbox:
                    test_started = time.monotonic()
                    try:
                        result = sandbox.commands.run(
                            sandbox_command,
                            user="root",
                            timeout=self.command_timeout_s,
                        )
                    except Exception as exc:
                        if not hasattr(exc, "exit_code"):
                            raise
                        result = exc
                    duration = time.monotonic() - test_started
                    memory_log = sandbox.files.read("/tmp/time.log")
                    peak_kb = parse_max_rss(str(memory_log))
                    runs.append(
                        BenchmarkRun(
                            cold_start_s=cold_start,
                            test_duration_s=duration,
                            peak_mem_mb=peak_kb / 1_024 if peak_kb >= 0 else -1,
                            exit_code=result.exit_code,
                        )
                    )
            except Exception:
                runs.append(
                    BenchmarkRun(
                        cold_start_s=time.monotonic() - started,
                        test_duration_s=float(self.command_timeout_s),
                        peak_mem_mb=-1,
                        exit_code=-1,
                    )
                )
        return summarize_runs(runs, test_cmd)


def subset_test_command(repo_path: Path, language: str, target_paths: list[str]) -> str | None:
    """Build a conservative test-subset command from LLM-proposed repository paths."""
    for raw_path in target_paths:
        relative = Path(raw_path.strip().lstrip("/"))
        if not relative.parts or ".." in relative.parts:
            continue
        candidate = repo_path / relative
        if not candidate.exists():
            continue
        target = relative if candidate.is_dir() else relative.parent
        if not target.parts or str(target) == ".":
            continue
        quoted = shlex.quote(target.as_posix())
        language = language.lower()
        if language == "go":
            return f"go test ./{target.as_posix().rstrip('/')}/..."
        if language == "python":
            return f"python -m pytest -x -q {quoted}"
        if language in {"typescript", "javascript"}:
            return f"CI=1 npm test -- {quoted}"
        if language == "rust":
            current = candidate if candidate.is_dir() else candidate.parent
            while current != repo_path and current.is_relative_to(repo_path):
                manifest = current / "Cargo.toml"
                if manifest.is_file():
                    manifest_path = manifest.relative_to(repo_path).as_posix()
                    return f"cargo test --manifest-path {shlex.quote(manifest_path)}"
                current = current.parent
    return None
