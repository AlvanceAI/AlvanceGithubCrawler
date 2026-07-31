from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .artifacts import write_text_atomic
from .jsonl_io import read_text_locked


def build_diversity_report(candidates_path: Path, *, feedback_path: Path | None = None) -> str:
    records = _read_jsonl(candidates_path)
    feedback = _read_jsonl(feedback_path) if feedback_path else []
    languages = Counter(str(record.get("language") or "unknown") for record in records)
    owners = Counter(str(record.get("repo") or "unknown").split("/", 1)[0] for record in records)
    taskability = Counter(_taskability_bucket(record) for record in records)
    contamination = Counter(_contamination_risk(record) for record in records)
    target_path_categories = Counter(_target_path_category(record) for record in records)
    taskability_risks = Counter(
        str(risk)
        for record in records
        for risk in ((record.get("taskability") or {}).get("risk") or [])
    )
    abandoned = {
        f"{item.get('repo')}@{item.get('base_commit')}"
        for item in feedback
        if item.get("outcome") == "abandoned"
    }
    lines = [
        "# Crawler Diversity Report\n\n",
        f"- Candidates: {len(records)}\n",
        f"- Abandoned feedback records: {len(abandoned)}\n",
        "\n## Languages\n\n",
        _render_counter(languages),
        "\n## Owners\n\n",
        _render_counter(owners.most_common(20)),
        "\n## Taskability\n\n",
        _render_counter(taskability),
        "\n## Taskability Risks\n\n",
        _render_counter(taskability_risks),
        "\n## Contamination Risk\n\n",
        _render_counter(contamination),
        "\n## Target Path Categories\n\n",
        _render_counter(target_path_categories),
        "\n## Abandoned Materials\n\n",
        _render_items(sorted(abandoned)),
        "\n## Warnings\n\n",
    ]
    warnings = _warnings(records, languages, contamination, target_path_categories, taskability)
    if not warnings:
        warnings.append("none")
    lines.extend(f"- {warning}\n" for warning in warnings)
    return "".join(lines)


def write_diversity_report(
    candidates_path: Path,
    out: Path,
    *,
    feedback_path: Path | None = None,
) -> str:
    report = build_diversity_report(candidates_path, feedback_path=feedback_path)
    write_text_atomic(out, report)
    return report


def _read_jsonl(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    records: list[dict[str, Any]] = []
    for line in read_text_locked(path).splitlines():
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            records.append(payload)
    return records


def _taskability_bucket(record: dict[str, Any]) -> str:
    score = ((record.get("taskability") or {}).get("score"))
    if not isinstance(score, (int, float)):
        return "unknown"
    if score >= 6:
        return "high"
    if score >= 3:
        return "medium"
    return "low"


def _contamination_risk(record: dict[str, Any]) -> str:
    contamination = record.get("contamination") or {}
    return str(contamination.get("risk") or contamination.get("status") or "unknown").lower()


def _target_path_category(record: dict[str, Any]) -> str:
    paths = [str(path) for path in _direction_target_paths(record)]
    if not paths:
        return "unknown"
    low_value_prefixes = ("docs/", "examples/", "example/", "website/", "demo/")
    if all(path.startswith(low_value_prefixes) for path in paths):
        return "low_value"
    if any(path.startswith(("src/", "pkg/", "lib/", "internal/", "packages/")) for path in paths):
        return "implementation"
    if any(path.startswith(("tests/", "test/")) for path in paths):
        return "tests"
    return "other"


def _direction_target_paths(record: dict[str, Any]) -> list[Any]:
    if record.get("direction_target_paths"):
        return list(record.get("direction_target_paths") or [])
    quality = record.get("quality") or {}
    direction = quality.get("direction") if isinstance(quality, dict) else {}
    if isinstance(direction, dict):
        return list(direction.get("target_paths") or [])
    return []


def _warnings(
    records: list[dict[str, Any]],
    languages: Counter[str],
    contamination: Counter[str],
    target_path_categories: Counter[str],
    taskability: Counter[str],
) -> list[str]:
    warnings: list[str] = []
    total = max(1, len(records))
    for language, count in languages.items():
        if count / total > 0.4:
            warnings.append(f"{language} exceeds 40% of candidates")
    for risk, count in contamination.items():
        if risk in {"high", "medium"} and count:
            warnings.append(f"{risk} contamination risk candidates: {count}")
    if target_path_categories.get("low_value", 0) / total > 0.2:
        warnings.append("low-value target paths exceed 20% of candidates")
    if taskability.get("low", 0) / total > 0.2:
        warnings.append("low taskability candidates exceed 20%")
    return warnings


def _render_counter(counter: Counter[str] | list[tuple[str, int]]) -> str:
    items = counter.items() if isinstance(counter, Counter) else counter
    rendered = [f"- `{key}`: {value}\n" for key, value in items]
    return "".join(rendered) if rendered else "- none\n"


def _render_items(items: list[str]) -> str:
    return "".join(f"- `{item}`\n" for item in items) if items else "- none\n"
