from __future__ import annotations

import fcntl
import logging
import os
import shutil
import subprocess
import tarfile
import tempfile
import time
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import requests

LOGGER = logging.getLogger(__name__)
MIB = 1024 * 1024
DEFAULT_WORKSPACE_MAX_MB = 50 * 1024
DEFAULT_WORKSPACE_RESERVATION_MB = 640
DEFAULT_WORKSPACE_QUOTA_WAIT_S = 900.0
SLOT_PREFIX = ".alvance-workspace-slot."


class CloneError(RuntimeError):
    pass


class WorkspaceQuotaError(CloneError):
    pass


def _run_git(args: list[str], *, cwd: Path | None = None, timeout: int = 60) -> None:
    result = subprocess.run(
        ["git", "-c", "http.version=HTTP/1.1", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        raise CloneError((result.stderr or result.stdout)[-2_000:])


@contextmanager
def cloned_repository(full_name: str, base_commit: str) -> Iterator[Path]:
    workspace_root = Path(_configured_workspace_tmpdir())
    with _workspace_quota_slot(workspace_root) as workspace_limit_bytes:
        with tempfile.TemporaryDirectory(
            prefix="alvance-repo-",
            dir=workspace_root,
        ) as temp_dir:
            path = Path(temp_dir)
            url = f"https://github.com/{full_name}.git"
            try:
                extracted = _download_tarball(
                    full_name,
                    base_commit,
                    path,
                    max_workspace_bytes=workspace_limit_bytes,
                )
            except WorkspaceQuotaError:
                raise
            except CloneError:
                shutil.rmtree(path, ignore_errors=True)
                path.mkdir(parents=True, exist_ok=True)
                _run_git(
                    ["clone", "--depth=1", "--no-tags", "--filter=blob:none", url, str(path)]
                )
                try:
                    _run_git(["checkout", "--detach", base_commit], cwd=path)
                except CloneError:
                    _run_git(["fetch", "--depth=1", "origin", base_commit], cwd=path)
                    _run_git(["checkout", "--detach", base_commit], cwd=path)
                _assert_workspace_size(path, workspace_limit_bytes)
                extracted = path
            # Single yield outside the except block: an exception raised inside the
            # caller's `with` body must not re-trigger the clone fallback path.
            yield extracted


def _configured_workspace_tmpdir() -> str:
    configured = os.environ.get("ALVANCE_WORKSPACE_TMPDIR", "").strip()
    path = (
        Path(configured).expanduser()
        if configured
        else Path.home() / ".cache" / "alvance-github-crawler" / "workspaces"
    )
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


@contextmanager
def _workspace_quota_slot(workspace_root: Path) -> Iterator[int]:
    max_mb = _positive_int_env("ALVANCE_WORKSPACE_MAX_MB", DEFAULT_WORKSPACE_MAX_MB)
    reservation_mb = _positive_int_env(
        "ALVANCE_WORKSPACE_RESERVATION_MB",
        DEFAULT_WORKSPACE_RESERVATION_MB,
    )
    if reservation_mb > max_mb:
        raise WorkspaceQuotaError(
            f"workspace reservation {reservation_mb}MB exceeds quota {max_mb}MB"
        )
    try:
        wait_s = float(
            os.environ.get(
                "ALVANCE_WORKSPACE_QUOTA_WAIT_S",
                str(DEFAULT_WORKSPACE_QUOTA_WAIT_S),
            )
        )
    except ValueError as exc:
        raise WorkspaceQuotaError("ALVANCE_WORKSPACE_QUOTA_WAIT_S must be numeric") from exc
    if wait_s < 0:
        raise WorkspaceQuotaError("ALVANCE_WORKSPACE_QUOTA_WAIT_S must be >= 0")

    workspace_root.mkdir(parents=True, exist_ok=True)
    maximum_slots = max_mb // reservation_mb
    slot_path = workspace_root / f"{SLOT_PREFIX}{os.getpid()}.{uuid.uuid4().hex}"
    lock_path = workspace_root / ".alvance-workspace-quota.lock"
    deadline = time.monotonic() + wait_s
    last_notice = 0.0

    while True:
        acquired = False
        with lock_path.open("a+", encoding="utf-8") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            _remove_stale_slots(workspace_root)
            active_slots = list(workspace_root.glob(f"{SLOT_PREFIX}*"))
            if len(active_slots) < maximum_slots:
                slot_path.write_text(f"{os.getpid()}\n", encoding="utf-8")
                acquired = True
        if acquired:
            break
        now = time.monotonic()
        if now >= deadline:
            raise WorkspaceQuotaError(
                f"workspace quota wait timed out: quota={max_mb}MB "
                f"reservation={reservation_mb}MB slots={maximum_slots}"
            )
        if now - last_notice >= 30:
            LOGGER.warning(
                "waiting for workspace quota slot quota_mb=%d reservation_mb=%d slots=%d",
                max_mb,
                reservation_mb,
                maximum_slots,
            )
            last_notice = now
        time.sleep(min(0.5, max(0.01, deadline - now)))

    try:
        yield reservation_mb * MIB
    finally:
        slot_path.unlink(missing_ok=True)


def _positive_int_env(name: str, default: int) -> int:
    try:
        value = int(os.environ.get(name, str(default)))
    except ValueError as exc:
        raise WorkspaceQuotaError(f"{name} must be an integer") from exc
    if value < 1:
        raise WorkspaceQuotaError(f"{name} must be >= 1")
    return value


def _remove_stale_slots(workspace_root: Path) -> None:
    for slot_path in workspace_root.glob(f"{SLOT_PREFIX}*"):
        parts = slot_path.name.removeprefix(SLOT_PREFIX).split(".", 1)
        try:
            pid = int(parts[0])
        except (IndexError, ValueError):
            continue
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            slot_path.unlink(missing_ok=True)
        except PermissionError:
            continue


def _download_tarball(
    full_name: str,
    base_commit: str,
    destination: Path,
    *,
    max_workspace_bytes: int,
) -> Path:
    url = f"https://codeload.github.com/{full_name}/tar.gz/{base_commit}"
    archive_path = destination / "repository.tar.gz"
    downloaded = 0
    started = time.monotonic()
    try:
        with requests.get(url, stream=True, timeout=(20, 60)) as response:
            response.raise_for_status()
            with archive_path.open("wb") as archive:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        downloaded += len(chunk)
                        if downloaded > 200 * 1024 * 1024:
                            raise CloneError("repository tarball exceeded 200 MB")
                        if time.monotonic() - started > 180:
                            raise CloneError("repository tarball download exceeded 180 seconds")
                        archive.write(chunk)
        with tarfile.open(archive_path, mode="r:gz") as tar:
            members = tar.getmembers()
            expanded_size = sum(max(0, int(member.size)) for member in members)
            if downloaded + expanded_size > max_workspace_bytes:
                raise WorkspaceQuotaError(
                    f"repository workspace requires at least "
                    f"{(downloaded + expanded_size) / MIB:.1f}MB; "
                    f"per-workspace limit is {max_workspace_bytes / MIB:.0f}MB"
                )
            tar.extractall(destination, members=members, filter="data")
    except CloneError:
        raise
    except (OSError, requests.RequestException, tarfile.TarError) as exc:
        raise CloneError(f"git clone and tarball fallback failed: {exc}") from exc
    archive_path.unlink(missing_ok=True)
    roots = [item for item in destination.iterdir() if item.is_dir()]
    if len(roots) != 1:
        raise CloneError(f"unexpected tarball layout for {full_name}@{base_commit}")
    return roots[0]


def _assert_workspace_size(path: Path, maximum_bytes: int) -> None:
    total = 0
    for root, _, files in os.walk(path):
        for name in files:
            try:
                total += (Path(root) / name).stat().st_size
            except OSError:
                continue
            if total > maximum_bytes:
                raise WorkspaceQuotaError(
                    f"repository checkout exceeded per-workspace limit "
                    f"{maximum_bytes / MIB:.0f}MB"
                )


def tree_summary(path: Path, *, max_entries: int = 1_500, max_chars: int = 18_000) -> str:
    ignored = {".git", "node_modules", "vendor", "target", "dist", "build", ".venv"}
    entries: list[str] = []
    for item in sorted(path.rglob("*")):
        try:
            relative = item.relative_to(path)
        except ValueError:
            continue
        if any(part in ignored for part in relative.parts):
            continue
        suffix = "/" if item.is_dir() else ""
        entries.append(f"{relative.as_posix()}{suffix}")
        if len(entries) >= max_entries:
            entries.append("... tree entry limit reached ...")
            break
    summary = "\n".join(entries)
    if len(summary) > max_chars:
        summary = summary[:max_chars] + "\n... tree character limit reached ..."
    return summary
