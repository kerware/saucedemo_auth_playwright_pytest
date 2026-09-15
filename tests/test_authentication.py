from __future__ import annotations

import pytest
from playwright.sync_api import Page

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.csv_loader import AuthenticationCase, load_authentication_cases


ALL_CASES = load_authentication_cases()
SUCCESS_CASES = [case for case in ALL_CASES if case.should_succeed]
ERROR_CASES = [case for case in ALL_CASES if not case.should_succeed]


@pytest.mark.authentication
@pytest.mark.parametrize("case", SUCCESS_CASES, ids=lambda case: case.case_id)
def test_authentification_acceptee(page: Page, case: AuthenticationCase) -> None:
    connexion = LoginPage(page)
    inventaire = InventoryPage(page)

    connexion.ouvrir_la_page_de_connexion()
    connexion.se_connecter_avec(case.username, case.password)
    inventaire.verifier_que_lutilisateur_est_connecte()


@pytest.mark.authentication
@pytest.mark.parametrize("case", ERROR_CASES, ids=lambda case: case.case_id)
def test_authentification_refusee(page: Page, case: AuthenticationCase) -> None:
    connexion = LoginPage(page)

    connexion.ouvrir_la_page_de_connexion()
    connexion.se_connecter_avec(case.username, case.password)
    connexion.verifier_le_message_derreur(case.expected_error)
    connexion.verifier_que_la_page_de_connexion_reste_affichee()
