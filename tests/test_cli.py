from __future__ import annotations

from alvance_github_crawler.cli import socks_proxy_configured


def test_socks_proxy_configured_detects_socks_environment(monkeypatch) -> None:
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        monkeypatch.delenv(key, raising=False)

    assert socks_proxy_configured() is False

    monkeypatch.setenv("ALL_PROXY", "socks5h://127.0.0.1:7890")

    assert socks_proxy_configured() is True
