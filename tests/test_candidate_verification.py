from __future__ import annotations

from dataclasses import dataclass

from alvance_github_crawler.e2b.verification import (
    benchmark_rejection,
    is_resource_e2b_error,
    is_transient_e2b_error,
)


@dataclass
class Benchmark:
    resource_pass: bool = True
    all_passed: bool = True
    flaky: bool = False


def test_benchmark_rejection_order() -> None:
    assert (
        benchmark_rejection(Benchmark(resource_pass=False), adjusted_score=9, minimum_score=7)
        == "benchmark_resource_fail"
    )
    assert (
        benchmark_rejection(Benchmark(all_passed=False), adjusted_score=9, minimum_score=7)
        == "benchmark_test_fail"
    )
    assert (
        benchmark_rejection(Benchmark(flaky=True), adjusted_score=6, minimum_score=7)
        == "flaky_adjusted_score=6"
    )
    assert benchmark_rejection(Benchmark(), adjusted_score=9, minimum_score=7) == ""


def test_transient_e2b_error_classification() -> None:
    assert is_transient_e2b_error(RuntimeError("HTTP 429: too many concurrent builds"))
    assert is_transient_e2b_error(RuntimeError("502 Bad Gateway"))
    assert not is_transient_e2b_error(RuntimeError("failed to run command 'npm ci': exit status 1"))


def test_resource_e2b_error_classification() -> None:
    assert is_resource_e2b_error(RuntimeError("compile: signal: killed"))
    assert is_resource_e2b_error(RuntimeError("rustc (signal: 9, SIGKILL: kill)"))
    assert is_resource_e2b_error(RuntimeError("exit_code=137"))
    assert not is_resource_e2b_error(RuntimeError("failed to run npm ci: exit status 1"))
