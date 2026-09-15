from __future__ import annotations

import logging
import re
from datetime import datetime
from pathlib import Path

import pytest
from playwright.sync_api import Page
from pytest_html import extras

from config.settings import SCREENSHOT_ON_FAILURE


PROJECT_ROOT = Path(__file__).resolve().parent
LOG_DIR = PROJECT_ROOT / "logs"
SCREENSHOT_DIR = PROJECT_ROOT / "reports" / "screenshots"


def pytest_configure(config: pytest.Config) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOG_DIR / f"actions_{timestamp}.log"

    logger = logging.getLogger("e2e.actions")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Évite l'empilement de handlers lors d'un lancement programmatique répété.
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    config._e2e_action_log_path = str(log_path)  # type: ignore[attr-defined]


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
        "ignore_https_errors": False,
    }


def _safe_filename(nodeid: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", nodeid).strip("_")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    outcome = yield
    report = outcome.get_result()

    if report.when not in {"setup", "call", "teardown"} or not report.failed:
        return

    page: Page | None = item.funcargs.get("page") if hasattr(item, "funcargs") else None
    if page is None or not SCREENSHOT_ON_FAILURE:
        return

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        screenshot_path = SCREENSHOT_DIR / f"{_safe_filename(item.nodeid)}_{report.when}_{timestamp}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)

        current_extras = list(getattr(report, "extras", []))
        current_extras.append(extras.image(str(screenshot_path), name="Capture en échec"))
        current_extras.append(extras.text(str(screenshot_path), name="Chemin capture"))
        report.extras = current_extras
    except Exception as exc:  # la collecte d'une preuve ne doit pas masquer l'échec initial
        logging.getLogger("e2e.actions").warning("Impossible de créer la capture d'échec : %s", exc)
