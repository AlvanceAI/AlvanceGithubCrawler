from __future__ import annotations

import re
import shlex
import statistics
import time
from pathlib import Path

from ..models import BenchmarkResult, BenchmarkRun
from ..runtime.profiles import command_with_environment, command_with_timeout

THRESHOLDS = {
    "cold_start_s": 20.0,
    "test_duration_s": 120.0,
    "peak_mem_mb": 4_096.0,
}
STABILITY_WINDOW_S = 15.0


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
    stable = max(durations) - min(durations) < STABILITY_WINDOW_S and len(set(exit_codes)) == 1
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
    def __init__(self, api_key: str, *, cpu_count: int = 1, memory_mb: int = 1_024) -> None:
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
        user: str = "root",
    ) -> BenchmarkResult:
        try:
            from e2b import Sandbox
        except ImportError as exc:
            raise RuntimeError("e2b SDK is not installed; install the project with [e2b]") from exc

        runs: list[BenchmarkRun] = []
        decisive_timeout_s = int(THRESHOLDS["test_duration_s"] + STABILITY_WINDOW_S)
        run_timeout_s = min(self.command_timeout_s, decisive_timeout_s)
        bounded_command = command_with_timeout(test_cmd, run_timeout_s)
        timed_command = f"/usr/bin/time -v -o /tmp/time.log sh -c {shlex.quote(bounded_command)}"
        sandbox_command = command_with_environment(timed_command, envs)
        for _ in range(self.runs):
            started = time.monotonic()
            try:
                sandbox = Sandbox.create(
                    template=template_id,
                    allow_internet_access=False,
                    timeout=run_timeout_s + 60,
                    envs=envs,
                    api_key=self.api_key,
                )
                cold_start = time.monotonic() - started
                with sandbox:
                    test_started = time.monotonic()
                    try:
                        result = sandbox.commands.run(
                            sandbox_command,
                            user=user,
                            timeout=run_timeout_s + 30,
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
                    if result.exit_code == 124:
                        break
            except Exception as exc:
                # Distinguish infrastructure failures (Sandbox.create, files.read, etc.)
                # from test-command failures so they are not silently treated as
                # benchmark runs and do not pollute flaky/stable classification.
                raise RuntimeError(
                    f"E2B infrastructure error during benchmark run: {exc}"
                ) from exc
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
            return f"go test ./{shlex.quote(target.as_posix().rstrip('/'))}/..."
        if language == "python":
            python_target = python_test_target(repo_path, relative, candidate)
            return f"python -m pytest -x -q {shlex.quote(python_target.as_posix())}"
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


def python_test_target(repo_path: Path, relative: Path, candidate: Path) -> Path:
    """Map src-layout targets to conventional pytest paths when available."""
    direct = relative if candidate.is_dir() else relative.parent
    if direct.parts and direct.parts[0] in {"test", "tests"}:
        return direct

    source_parts = list(relative.parts)
    if source_parts and source_parts[0] == "src":
        source_parts.pop(0)
    if not source_parts:
        return direct

    leaf = Path(source_parts[-1]).stem
    names = (f"test_{leaf}", leaf, f"test_{leaf}.py")
    candidates = [Path("tests") / name for name in names]
    if len(source_parts) > 1:
        parent = Path("tests", *source_parts[:-1])
        candidates.extend(parent / name for name in names)
    for test_target in candidates:
        if (repo_path / test_target).exists():
            return test_target
    return direct
