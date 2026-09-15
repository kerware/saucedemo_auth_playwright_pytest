from __future__ import annotations

from playwright.sync_api import Locator, Page, expect

from config.settings import DEFAULT_TIMEOUT_MS
from utils.action_logger import ActionLogger


class BasePage:
    def __init__(self, page: Page, component_name: str) -> None:
        self.page = page
        self.timeout = DEFAULT_TIMEOUT_MS
        self.log = ActionLogger(component_name)
        self.page.set_default_timeout(self.timeout)

    def _attendre_visible(self, locator: Locator, description: str) -> None:
        self.log.info(f"Attente de visibilité : {description}")
        locator.wait_for(state="visible", timeout=self.timeout)

    def _attendre_saisissable(self, locator: Locator, description: str) -> None:
        self._attendre_visible(locator, description)
        expect(locator).to_be_editable(timeout=self.timeout)

    def _attendre_cliquable(self, locator: Locator, description: str) -> None:
        self._attendre_visible(locator, description)
        expect(locator).to_be_enabled(timeout=self.timeout)
