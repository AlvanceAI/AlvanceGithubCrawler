from __future__ import annotations

import json
import re
import shutil
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .artifacts import write_json_atomic, write_text_atomic
from .deepswe_handoff import candidate_to_handoff
from .repo_summary import candidate_to_repo_summary

LANGUAGE_ORDER = ("python", "go", "typescript", "javascript", "rust")
CLONE_ERROR_TAIL_CHARS = 4_000

ProgressCallback = Callable[[int, int, str], None]
AdvanceCallback = Callable[[], None]


def load_candidate_records(crawler_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    candidates_path = crawler_dir / ".crawler-state" / "candidates.jsonl"
    if candidates_path.is_file():
        records.extend(
            normalize_registry_record(item) for item in latest_by_repo(read_jsonl(candidates_path))
        )
    packages_path = crawler_dir / "catalog" / "e2b-packages.jsonl"
    if packages_path.is_file():
        records.extend(
            normalize_package_record(crawler_dir, item)
            for item in read_jsonl(packages_path)
        )

    unique: dict[str, dict[str, Any]] = {}
    for record in records:
        if usable_record(record):
            unique[str(record["repo"])] = record
    return list(unique.values())


def normalize_registry_record(record: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(record)
    repo = normalized.get("repo")
    normalized.setdefault("repository_url", f"https://github.com/{repo}" if repo else None)
    normalized.setdefault(
        "direction_source",
        normalized.get("direction_source") or "crawler:candidate",
    )
    package = normalized.get("harbor_package") or {}
    if isinstance(package, dict):
        normalized.setdefault("material_path", package.get("material_path"))
        normalized.setdefault("task_path", package.get("task_path"))
    return normalized


def normalize_package_record(crawler_dir: Path, record: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(record)
    repo = normalized.get("repo")
    task_path = normalized.get("task_path")
    material_path = normalized.get("material_path")
    quality = normalized.get("quality") if isinstance(normalized.get("quality"), dict) else {}
    direction_quality = quality.get("direction") if isinstance(quality, dict) else {}
    if not isinstance(direction_quality, dict):
        direction_quality = {}

    direction = (
        str(normalized.get("direction") or "")
        or read_existing_direction(crawler_dir, task_path)
        or default_direction(normalized)
    )
    normalized.setdefault("repository_url", f"https://github.com/{repo}" if repo else None)
    normalized["direction"] = direction
    normalized.setdefault("direction_source", "crawler:existing_material")
    normalized.setdefault(
        "direction_keywords",
        direction_quality.get("keywords") or infer_keywords(direction),
    )
    normalized.setdefault(
        "direction_target_paths",
        direction_quality.get("target_paths") or [],
    )
    normalized["benchmark"] = normalized.get("benchmark") or normalized.get("verification") or {}
    normalized.setdefault(
        "taskability",
        quality.get("taskability")
        or {"score": 7 if normalized.get("status") == "qualified" else 4, "risk": []},
    )
    normalized.setdefault(
        "contamination",
        quality.get("contamination")
        or {
            "risk": "unknown",
            "notes": (
                "Existing Crawler material did not include final DeepSWE "
                "contamination metadata."
            ),
        },
    )
    normalized.setdefault("e2b_template", e2b_metadata(normalized)["source_template_alias"])
    normalized.setdefault("e2b_environment", package_environment(normalized))
    normalized["harbor_package"] = {
        "material_path": material_path,
        "task_path": task_path,
        "harbor": normalized.get("harbor") or {},
        "e2b_history": normalized.get("e2b_history") or {},
    }
    return normalized


def package_environment(record: dict[str, Any]) -> dict[str, Any]:
    resources = record.get("resources") or {}
    if not isinstance(resources, dict):
        resources = {}
    payload = {
        "runtime_version": record.get("runtime_version"),
        "runtime_env": record.get("runtime_env"),
        "execution_user": record.get("execution_user"),
        "cpu_count": resources.get("cpu_count"),
        "memory_mb": resources.get("memory_mb"),
    }
    return {key: value for key, value in payload.items() if value not in (None, "", {})}


def has_ready_e2b_material(record: dict[str, Any]) -> bool:
    metadata = e2b_metadata(record)
    return bool(metadata["harbor_template_alias"] and metadata["harbor_template_id"])


def e2b_metadata(record: dict[str, Any]) -> dict[str, str]:
    package = record.get("harbor_package") or {}
    if not isinstance(package, dict):
        package = {}
    harbor = package.get("harbor") or record.get("harbor") or {}
    if not isinstance(harbor, dict):
        harbor = {}
    history = package.get("e2b_history") or record.get("e2b_history") or {}
    if not isinstance(history, dict):
        history = {}
    history_source = history.get("source_template") or {}
    history_harbor = history.get("harbor_template") or {}
    source_template = record.get("source_template") or {}
    environment = record.get("e2b_environment") or {}
    if not isinstance(history_source, dict):
        history_source = {}
    if not isinstance(history_harbor, dict):
        history_harbor = {}
    if not isinstance(source_template, dict):
        source_template = {}
    if not isinstance(environment, dict):
        environment = {}
    return {
        "material_path": str(package.get("material_path") or record.get("material_path") or ""),
        "task_path": str(package.get("task_path") or record.get("task_path") or ""),
        "source_template_alias": str(
            history_source.get("alias")
            or source_template.get("alias")
            or record.get("e2b_template")
            or ""
        ),
        "source_template_id": str(
            history_source.get("template_id") or source_template.get("template_id") or ""
        ),
        "harbor_template_alias": str(
            history_harbor.get("alias") or harbor.get("template_alias") or ""
        ),
        "harbor_template_id": str(
            history_harbor.get("template_id") or harbor.get("template_id") or ""
        ),
        "harbor_launch_command": str(harbor.get("launch_command") or ""),
        "runtime_version": str(
            record.get("runtime_version") or environment.get("runtime_version") or ""
        ),
        "execution_user": str(
            record.get("execution_user") or environment.get("execution_user") or ""
        ),
        "test_cmd": str(record.get("test_cmd") or ""),
    }


def usable_record(record: dict[str, Any]) -> bool:
    required = ("repo", "repository_url", "base_commit", "language", "direction")
    if any(not record.get(key) for key in required):
        return False
    status = str(record.get("status") or "qualified")
    return status in {"qualified", "ready_for_phase1", "offline_verified", "offline_verified_local"}


def latest_by_repo(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for record in records:
        repo = record.get("repo")
        if repo:
            latest[str(repo)] = record
    return list(latest.values())


def select_records(
    records: list[dict[str, Any]],
    repo_count: int,
) -> tuple[list[dict[str, Any]], list[str]]:
    warnings: list[str] = []
    by_language: dict[str, list[dict[str, Any]]] = {}
    for record in sorted(records, key=record_score, reverse=True):
        language = str(record.get("language") or "unknown").lower()
        by_language.setdefault(language, []).append(record)

    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for language in LANGUAGE_ORDER:
        if len(selected) >= repo_count:
            break
        for record in by_language.get(language, []):
            repo = str(record["repo"])
            if repo not in seen:
                selected.append(record)
                seen.add(repo)
                break

    for record in sorted(records, key=record_score, reverse=True):
        if len(selected) >= repo_count:
            break
        repo = str(record["repo"])
        if repo not in seen:
            selected.append(record)
            seen.add(repo)

    languages = sorted({str(item.get("language") or "unknown").lower() for item in selected})
    if len(languages) < min(repo_count, len(LANGUAGE_ORDER)):
        warnings.append(
            "selected materials do not cover five languages; "
            "run with production credentials for broader coverage"
        )
    return selected, warnings


def record_score(record: dict[str, Any]) -> float:
    score = float(record.get("adjusted_score") or record.get("soft_score") or 0)
    taskability = record.get("taskability") or {}
    if isinstance(taskability, dict):
        score += float(taskability.get("score") or 0)
    benchmark = record.get("benchmark") or record.get("verification") or {}
    if isinstance(benchmark, dict):
        if benchmark.get("offline_ok") is True:
            score += 3
        if benchmark.get("stable") is True:
            score += 2
        duration = benchmark.get("test_duration_median_s")
        if isinstance(duration, (int, float)) and duration <= 30:
            score += 1
    return score


def prepare_materials(
    records: list[dict[str, Any]],
    *,
    crawler_dir: Path,
    material_dir: Path,
    clone_repos: bool,
    require_clone: bool,
    clone_timeout_s: int,
    on_step: ProgressCallback | None = None,
    on_advance: AdvanceCallback | None = None,
) -> list[dict[str, Any]]:
    handoff_dir = material_dir / "handoff"
    summary_dir = material_dir / "repo-summary"
    material_copy_root = material_dir / "materials"
    crawler_task_root = material_dir / "crawler-tasks"
    repo_root = material_dir / "repos"
    for directory in (handoff_dir, summary_dir, material_copy_root, crawler_task_root, repo_root):
        directory.mkdir(parents=True, exist_ok=True)

    index: list[dict[str, Any]] = []
    selected_jsonl: list[str] = []
    total = len(records)
    for position, record in enumerate(records, start=1):
        repo_slug = slugify(str(record["repo"]))
        emit_step(on_step, position, total, f"preparing {record['repo']}")
        handoff = candidate_to_handoff(record)
        summary = candidate_to_repo_summary(record)
        handoff_path = handoff_dir / f"{repo_slug}.json"
        summary_path = summary_dir / f"{repo_slug}.summary.json"
        write_json_atomic(handoff_path, handoff)
        write_json_atomic(summary_path, summary)
        selected_jsonl.append(json.dumps(record, ensure_ascii=False, sort_keys=True))

        copied_material = copy_relative_tree(
            crawler_dir,
            record.get("material_path"),
            material_copy_root / repo_slug,
        )
        copied_task = copy_relative_tree(
            crawler_dir,
            record.get("task_path"),
            crawler_task_root / repo_slug,
        )
        checkout = None
        clone_status = "skipped"
        if clone_repos:
            emit_step(
                on_step,
                position,
                total,
                f"cloning {record['repo']} at {record['base_commit']}",
            )
            checkout, clone_status = clone_repo(
                record,
                repo_root / repo_slug,
                timeout_s=clone_timeout_s,
            )
            if require_clone and clone_status != "ok":
                raise RuntimeError(f"clone failed for {record['repo']}: {clone_status}")
            emit_step(on_step, position, total, f"{record['repo']} clone status: {clone_status}")
        else:
            write_checkout_readme(repo_root / repo_slug, record)

        index.append(
            {
                "repo": record["repo"],
                "language": record.get("language"),
                "base_commit": record.get("base_commit"),
                "e2b": e2b_metadata(record),
                "handoff": str(handoff_path),
                "repo_summary": str(summary_path),
                "material_copy": str(copied_material) if copied_material else None,
                "crawler_task_copy": str(copied_task) if copied_task else None,
                "checkout": str(checkout) if checkout else None,
                "clone_status": clone_status,
            }
        )
        if on_advance:
            on_advance()
    write_text_atomic(material_dir / "selected-candidates.jsonl", "\n".join(selected_jsonl) + "\n")
    return index


def emit_step(callback: ProgressCallback | None, current: int, total: int, message: str) -> None:
    if callback:
        callback(current, total, message)


def copy_relative_tree(root: Path, relative: Any, destination: Path) -> Path | None:
    if not relative:
        return None
    source = root / str(relative)
    if not source.exists():
        return None
    if destination.exists():
        shutil.rmtree(destination)
    if source.is_dir():
        shutil.copytree(source, destination)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    return destination


def clone_repo(
    record: dict[str, Any],
    destination: Path,
    *,
    timeout_s: int,
) -> tuple[Path | None, str]:
    if destination.is_dir() and (destination / ".git").is_dir():
        return destination, "existing"
    if destination.exists():
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "git",
        "clone",
        "--filter=blob:none",
        str(record["repository_url"]),
        str(destination),
    ]
    result = run_timed(command, timeout_s=timeout_s)
    if result.returncode != 0:
        write_checkout_error(destination, record, result.stdout)
        return None, "clone_failed"
    checkout = run_timed(
        ["git", "-C", str(destination), "checkout", str(record["base_commit"])],
        timeout_s=timeout_s,
    )
    if checkout.returncode != 0:
        write_checkout_error(destination, record, checkout.stdout)
        return None, "checkout_failed"
    return destination, "ok"


def run_timed(command: list[str], *, timeout_s: int) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_s,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        return subprocess.CompletedProcess(
            args=command,
            returncode=124,
            stdout=output + f"\nTimed out after {timeout_s}s",
            stderr=None,
        )


def write_checkout_readme(destination: Path, record: dict[str, Any]) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    write_text_atomic(
        destination / "README.checkout.md",
        f"""# Checkout skipped

Repository: {record.get("repository_url")}
Commit: {record.get("base_commit")}

Run the material export with `--clone-repos` in a network-enabled environment to place
the source checkout here.
""",
    )


def write_checkout_error(destination: Path, record: dict[str, Any], output: str) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    write_text_atomic(
        destination / "CLONE_FAILED.txt",
        (
            f"Repository: {record.get('repository_url')}\n"
            f"Commit: {record.get('base_commit')}\n\n"
            f"{output[-CLONE_ERROR_TAIL_CHARS:]}\n"
        ),
    )


def read_existing_direction(crawler_dir: Path, task_path: Any) -> str:
    if not task_path:
        return ""
    direction_path = crawler_dir / str(task_path) / "direction.md"
    if direction_path.is_file():
        text = direction_path.read_text(encoding="utf-8", errors="replace")
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip() and not line.startswith("#")
        ]
        if lines:
            return clean_inline(lines[0])
    return ""


def default_direction(record: dict[str, Any]) -> str:
    repo = str(record.get("repo") or "the project")
    language = str(record.get("language") or "the supported runtime")
    return (
        f"Add a focused behavior extension for {repo} "
        f"that exercises its {language} public surface."
    )


def infer_keywords(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", text)
    return list(dict.fromkeys(words[:5]))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            records.append(payload)
    return records


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def clean_inline(value: str) -> str:
    return " ".join(value.strip().split())
