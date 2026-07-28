from __future__ import annotations

import shutil
import subprocess
import tarfile
import tempfile
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import requests


class CloneError(RuntimeError):
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
    with tempfile.TemporaryDirectory(prefix="alvance-repo-") as temp_dir:
        path = Path(temp_dir)
        url = f"https://github.com/{full_name}.git"
        try:
            extracted = _download_tarball(full_name, base_commit, path)
            yield extracted
        except CloneError:
            shutil.rmtree(path, ignore_errors=True)
            path.mkdir(parents=True, exist_ok=True)
            _run_git(["clone", "--depth=1", "--no-tags", "--filter=blob:none", url, str(path)])
            try:
                _run_git(["checkout", "--detach", base_commit], cwd=path)
            except CloneError:
                _run_git(["fetch", "--depth=1", "origin", base_commit], cwd=path)
                _run_git(["checkout", "--detach", base_commit], cwd=path)
            yield path


def _download_tarball(full_name: str, base_commit: str, destination: Path) -> Path:
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
            tar.extractall(destination, filter="data")
    except CloneError:
        raise
    except (OSError, requests.RequestException, tarfile.TarError) as exc:
        raise CloneError(f"git clone and tarball fallback failed: {exc}") from exc
    archive_path.unlink(missing_ok=True)
    roots = [item for item in destination.iterdir() if item.is_dir()]
    if len(roots) != 1:
        raise CloneError(f"unexpected tarball layout for {full_name}@{base_commit}")
    return roots[0]


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
