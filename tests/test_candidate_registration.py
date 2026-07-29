from __future__ import annotations

from alvance_github_crawler.pending.registration import compact_environment


def test_compact_environment_removes_remote_test_logs() -> None:
    original = {
        "runtime_version": "1.26.5",
        "offline": {
            "ok": True,
            "duration_s": 4.2,
            "stdout_tail": "large stdout",
            "stderr_tail": "large stderr",
        },
    }

    compact = compact_environment(original)

    assert compact == {
        "runtime_version": "1.26.5",
        "offline": {"ok": True, "duration_s": 4.2},
    }
    assert "stdout_tail" in original["offline"]


def test_compact_environment_preserves_none() -> None:
    assert compact_environment(None) is None
