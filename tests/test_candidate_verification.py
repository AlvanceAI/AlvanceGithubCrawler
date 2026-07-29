from __future__ import annotations

from dataclasses import dataclass

from alvance_github_crawler.e2b.verification import (
    E2BCandidateVerifier,
    benchmark_rejection,
    is_e2b_key_exhausted_error,
    is_resource_e2b_error,
    is_transient_e2b_error,
)
from alvance_github_crawler.runtime.profiles import UnsupportedRuntimeError


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


def test_e2b_key_exhaustion_classification() -> None:
    assert is_e2b_key_exhausted_error(RuntimeError("HTTP 402: payment required"))
    assert is_e2b_key_exhausted_error(RuntimeError("not enough credits to build template"))
    assert not is_e2b_key_exhausted_error(RuntimeError("too many concurrent sandboxes"))


def test_unsupported_runtime_is_a_terminal_rejection(tmp_path) -> None:
    rejected: list[tuple[str, str]] = []

    class Environment:
        @staticmethod
        def ensure(repo, repo_path, base_commit):
            raise UnsupportedRuntimeError("requires Python 3.14")

    class Registry:
        @staticmethod
        def reject(repo, stage, reason, **details):
            rejected.append((stage, reason))

    verifier = E2BCandidateVerifier.__new__(E2BCandidateVerifier)
    verifier.environment = Environment()  # type: ignore[assignment]
    verifier.registry = Registry()  # type: ignore[assignment]

    outcome = verifier.verify(
        {"full_name": "owner/repository", "base_commit": "a" * 40},
        tmp_path,
        score={"total": 10},
        direction={},
    )

    assert outcome == "rejected"
    assert rejected == [("stage3_5_e2b_environment", "unsupported_runtime")]
