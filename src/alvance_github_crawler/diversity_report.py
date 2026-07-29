from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .artifacts import write_text_atomic


def build_diversity_report(candidates_path: Path, *, feedback_path: Path | None = None) -> str:
    records = _read_jsonl(candidates_path)
    feedback = _read_jsonl(feedback_path) if feedback_path else []
    languages = Counter(str(record.get("language") or "unknown") for record in records)
    owners = Counter(str(record.get("repo") or "unknown").split("/", 1)[0] for record in records)
    taskability = Counter(_taskability_bucket(record) for record in records)
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
        "\n## Warnings\n\n",
    ]
    warnings = []
    total = max(1, len(records))
    for language, count in languages.items():
        if count / total > 0.4:
            warnings.append(f"{language} exceeds 40% of candidates")
    if not warnings:
        warnings.append("none")
    lines.extend(f"- {warning}\n" for warning in warnings)
    return "".join(lines)


def write_diversity_report(candidates_path: Path, out: Path, *, feedback_path: Path | None = None) -> str:
    report = build_diversity_report(candidates_path, feedback_path=feedback_path)
    write_text_atomic(out, report)
    return report


def _read_jsonl(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
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


def _render_counter(counter: Counter[str] | list[tuple[str, int]]) -> str:
    items = counter.items() if isinstance(counter, Counter) else counter
    rendered = [f"- `{key}`: {value}\n" for key, value in items]
    return "".join(rendered) if rendered else "- none\n"
