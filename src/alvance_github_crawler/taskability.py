from __future__ import annotations

from typing import Any

POSITIVE_DOMAINS = {
    "cache",
    "cli",
    "client",
    "compiler",
    "config",
    "formatter",
    "linter",
    "orm",
    "parser",
    "protocol",
    "sdk",
    "serializer",
    "toolkit",
}

LOW_VALUE_PATHS = ("docs/", "examples/", "example/", "website/", "demo/")


def evaluate_taskability(
    repo: dict[str, Any],
    *,
    direction: dict[str, Any] | None = None,
    benchmark: dict[str, Any] | None = None,
) -> dict[str, Any]:
    direction = direction or {}
    text = " ".join(
        [
            str(repo.get("name") or ""),
            str(repo.get("description") or ""),
            " ".join(str(topic) for topic in repo.get("topics") or []),
            str(direction.get("direction") or ""),
        ]
    ).lower()
    score = 0
    signals: list[str] = []
    for signal in sorted(POSITIVE_DOMAINS):
        if signal in text:
            score += 1
            signals.append(signal)

    target_paths = [str(path) for path in direction.get("target_paths") or []]
    if target_paths and all(path.startswith(LOW_VALUE_PATHS) for path in target_paths):
        score -= 2
        signals.append("low_value_target_paths")

    test_duration = (benchmark or {}).get("test_duration_median_s")
    if isinstance(test_duration, (int, float)) and test_duration < 120:
        score += 1
        signals.append("test_budget_ok")

    return {
        "schema_version": "0.1",
        "score": max(0, min(10, score)),
        "signals": signals,
        "risk": ["low_taskability"] if score <= 1 else [],
    }
