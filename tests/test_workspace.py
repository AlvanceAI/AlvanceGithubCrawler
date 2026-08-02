from __future__ import annotations

from pathlib import Path

import pytest

from alvance_github_crawler import workspace


def test_cloned_repository_uses_disk_workspace_override(tmp_path, monkeypatch) -> None:
    workspace_root = tmp_path / "workspace"
    destinations: list[Path] = []

    def fake_download(
        full_name: str,
        base_commit: str,
        destination: Path,
        *,
        max_workspace_bytes: int,
    ) -> Path:
        destinations.append(destination)
        assert max_workspace_bytes == 640 * 1024 * 1024
        extracted = destination / "repository"
        extracted.mkdir()
        return extracted

    monkeypatch.setenv("ALVANCE_WORKSPACE_TMPDIR", str(workspace_root))
    monkeypatch.setattr(workspace, "_download_tarball", fake_download)

    with workspace.cloned_repository("owner/repository", "a" * 40) as repo_path:
        assert repo_path.parent.parent == workspace_root
        assert repo_path.is_dir()

    assert len(destinations) == 1
    assert not destinations[0].exists()
    assert list(workspace_root.glob(f"{workspace.SLOT_PREFIX}*")) == []


def test_workspace_quota_bounds_cross_process_slots(tmp_path, monkeypatch) -> None:
    workspace_root = tmp_path / "workspace"
    monkeypatch.setenv("ALVANCE_WORKSPACE_MAX_MB", "1280")
    monkeypatch.setenv("ALVANCE_WORKSPACE_RESERVATION_MB", "640")
    monkeypatch.setenv("ALVANCE_WORKSPACE_QUOTA_WAIT_S", "0")

    with workspace._workspace_quota_slot(workspace_root) as first_limit:
        with workspace._workspace_quota_slot(workspace_root) as second_limit:
            assert first_limit == second_limit == 640 * 1024 * 1024
            with pytest.raises(workspace.WorkspaceQuotaError, match="quota wait timed out"):
                with workspace._workspace_quota_slot(workspace_root):
                    pass

    assert list(workspace_root.glob(f"{workspace.SLOT_PREFIX}*")) == []


def test_workspace_size_limit_rejects_large_checkout(tmp_path) -> None:
    (tmp_path / "large.bin").write_bytes(b"x" * 1025)

    with pytest.raises(workspace.WorkspaceQuotaError, match="exceeded"):
        workspace._assert_workspace_size(tmp_path, 1024)
