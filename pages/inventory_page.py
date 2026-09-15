from __future__ import annotations

import re

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from resources.locators import InventoryLocators


class InventoryPage(BasePage):
    """Page Object de la liste des produits et de son panier."""

    def __init__(self, page: Page) -> None:
        super().__init__(page, "Inventaire")
        self._title = page.locator(InventoryLocators.TITLE)
        self._inventory_list = page.locator(InventoryLocators.INVENTORY_LIST)
        self._products = page.locator(InventoryLocators.PRODUCT_ITEM)
        self._cart_link = page.locator(InventoryLocators.SHOPPING_CART_LINK)
        self._cart_badge = page.locator(InventoryLocators.SHOPPING_CART_BADGE)

    def verifier_que_lutilisateur_est_connecte(self) -> None:
        self.log.info("Vérification de l'arrivée sur l'écran Produits")
        expect(self.page).to_have_url(re.compile(r".*/inventory\.html(?:[?#].*)?$"), timeout=self.timeout)
        self._attendre_visible(self._title, "titre Products")
        self._attendre_visible(self._inventory_list, "liste des produits")

    def _carte_produit(self, nom_produit: str):
        return self._products.filter(has_text=nom_produit).first

    def ajouter_le_produit_au_panier(self, nom_produit: str) -> None:
        self.log.info(f"Ajout du produit au panier : {nom_produit!r}")
        carte = self._carte_produit(nom_produit)
        expect(carte).to_be_visible(timeout=self.timeout)
        bouton = carte.locator(InventoryLocators.ADD_TO_CART_BUTTON)
        self._attendre_cliquable(bouton, f"bouton d'ajout de {nom_produit}")
        bouton.click()

    def verifier_le_nombre_de_produits_dans_le_panier(self, nombre_attendu: int) -> None:
        self.log.info(f"Vérification du nombre de produits dans le panier : {nombre_attendu}")
        if nombre_attendu == 0:
            expect(self._cart_badge).to_have_count(0, timeout=self.timeout)
            return
        self._attendre_visible(self._cart_badge, "compteur du panier")
        expect(self._cart_badge).to_have_text(str(nombre_attendu), timeout=self.timeout)

    def ouvrir_le_panier(self) -> None:
        self.log.info("Ouverture du panier")
        self._attendre_cliquable(self._cart_link, "lien du panier")
        self._cart_link.click()
