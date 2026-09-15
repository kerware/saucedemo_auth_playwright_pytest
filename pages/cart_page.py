from __future__ import annotations

import re
from collections.abc import Iterable

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from resources.locators import CartLocators


class CartPage(BasePage):
    """Page Object de la page panier."""

    def __init__(self, page: Page) -> None:
        super().__init__(page, "Panier")
        self._title = page.locator(CartLocators.TITLE)
        self._cart_list = page.locator(CartLocators.CART_LIST)
        self._items = page.locator(CartLocators.CART_ITEM)

    def verifier_que_le_panier_est_affiche(self) -> None:
        self.log.info("Vérification de l'affichage du panier")
        expect(self.page).to_have_url(re.compile(r".*/cart\.html(?:[?#].*)?$"), timeout=self.timeout)
        self._attendre_visible(self._title, "titre Your Cart")
        self._attendre_visible(self._cart_list, "liste du panier")

    def verifier_que_le_panier_contient(self, noms_produits: Iterable[str]) -> None:
        produits = list(noms_produits)
        self.log.info(f"Vérification des produits du panier : {produits!r}")
        expect(self._items).to_have_count(len(produits), timeout=self.timeout)
        for nom_produit in produits:
            article = self._items.filter(has_text=nom_produit).first
            expect(article.locator(CartLocators.ITEM_NAME)).to_have_text(
                nom_produit, timeout=self.timeout
            )

    def supprimer_le_produit(self, nom_produit: str) -> None:
        self.log.info(f"Suppression du produit du panier : {nom_produit!r}")
        article = self._items.filter(has_text=nom_produit).first
        expect(article).to_be_visible(timeout=self.timeout)
        bouton = article.locator(CartLocators.REMOVE_BUTTON)
        self._attendre_cliquable(bouton, f"bouton de suppression de {nom_produit}")
        bouton.click()

    def verifier_que_le_panier_est_vide(self) -> None:
        self.log.info("Vérification que le panier est vide")
        expect(self._items).to_have_count(0, timeout=self.timeout)
