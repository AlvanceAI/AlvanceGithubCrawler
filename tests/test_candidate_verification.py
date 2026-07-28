from __future__ import annotations

from dataclasses import dataclass

from alvance_github_crawler.candidate_verification import benchmark_rejection


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
