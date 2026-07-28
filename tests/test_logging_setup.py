from __future__ import annotations

import logging

from alvance_github_crawler.logging_setup import NETWORK_LOGGERS, configure_logging


def test_verbose_logging_keeps_network_libraries_quiet() -> None:
    configure_logging(verbose=True)

    assert logging.getLogger("alvance_github_crawler").level == logging.DEBUG
    assert all(logging.getLogger(name).level == logging.WARNING for name in NETWORK_LOGGERS)


def test_default_logging_keeps_crawler_at_info() -> None:
    configure_logging(verbose=False)

    assert logging.getLogger("alvance_github_crawler").level == logging.INFO
