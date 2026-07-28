from __future__ import annotations

import logging

NETWORK_LOGGERS = (
    "e2b",
    "h2",
    "hpack",
    "httpcore",
    "httpx",
    "openai",
    "requests",
    "urllib3",
)


def configure_logging(*, verbose: bool) -> None:
    """Enable crawler diagnostics without exposing third-party request headers."""
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logging.getLogger("alvance_github_crawler").setLevel(logging.DEBUG if verbose else logging.INFO)
    for logger_name in NETWORK_LOGGERS:
        logging.getLogger(logger_name).setLevel(logging.WARNING)
