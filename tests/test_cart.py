from __future__ import annotations

import pytest
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.csv_loader import (
    CartProductCase,
    load_authentication_cases,
    load_cart_products,
)


STANDARD_USER = next(
    case for case in load_authentication_cases() if case.username == "standard_user"
)
PRODUCT_CASES = load_cart_products()


def _ouvrir_un_panier(page: Page) -> tuple[InventoryPage, CartPage]:
    connexion = LoginPage(page)
    inventaire = InventoryPage(page)
    panier = CartPage(page)

    connexion.ouvrir_la_page_de_connexion()
    connexion.se_connecter_avec(STANDARD_USER.username, STANDARD_USER.password)
    inventaire.verifier_que_lutilisateur_est_connecte()
    return inventaire, panier


@pytest.mark.cart
@pytest.mark.parametrize("product", PRODUCT_CASES, ids=lambda case: case.case_id)
def test_ajouter_un_produit_au_panier(page: Page, product: CartProductCase) -> None:
    inventaire, panier = _ouvrir_un_panier(page)

    inventaire.ajouter_le_produit_au_panier(product.product_name)
    inventaire.verifier_le_nombre_de_produits_dans_le_panier(1)
    inventaire.ouvrir_le_panier()

    panier.verifier_que_le_panier_est_affiche()
    panier.verifier_que_le_panier_contient([product.product_name])


@pytest.mark.cart
def test_ajouter_plusieurs_produits_au_panier(page: Page) -> None:
    inventaire, panier = _ouvrir_un_panier(page)
    produits = [product.product_name for product in PRODUCT_CASES[:2]]

    for produit in produits:
        inventaire.ajouter_le_produit_au_panier(produit)
    inventaire.verifier_le_nombre_de_produits_dans_le_panier(len(produits))
    inventaire.ouvrir_le_panier()

    panier.verifier_que_le_panier_est_affiche()
    panier.verifier_que_le_panier_contient(produits)


@pytest.mark.cart
def test_supprimer_un_produit_du_panier(page: Page) -> None:
    inventaire, panier = _ouvrir_un_panier(page)
    produits = [product.product_name for product in PRODUCT_CASES[:2]]

    for produit in produits:
        inventaire.ajouter_le_produit_au_panier(produit)
    inventaire.ouvrir_le_panier()
    panier.verifier_que_le_panier_contient(produits)

    panier.supprimer_le_produit(produits[0])
    panier.verifier_que_le_panier_contient([produits[1]])
