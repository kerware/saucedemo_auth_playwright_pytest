from __future__ import annotations

import re

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from resources.locators import InventoryLocators


class InventoryPage(BasePage):
    """Page Object minimal de l'écran cible après authentification réussie.

    Aucun test métier d'inventaire n'est réalisé : cet écran sert uniquement
    d'oracle pour confirmer le succès de l'authentification.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page, "Inventaire")
        self._title = page.locator(InventoryLocators.TITLE)
        self._inventory_list = page.locator(InventoryLocators.INVENTORY_LIST)

    def verifier_que_lutilisateur_est_connecte(self) -> None:
        self.log.info("Vérification de l'arrivée sur l'écran Produits")
        expect(self.page).to_have_url(re.compile(r".*/inventory\.html(?:[?#].*)?$"), timeout=self.timeout)
        self._attendre_visible(self._title, "titre Products")
        self._attendre_visible(self._inventory_list, "liste des produits")
