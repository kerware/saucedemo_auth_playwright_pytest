from __future__ import annotations

from playwright.sync_api import Page, expect

from config.settings import BASE_URL
from pages.base_page import BasePage
from resources.locators import LoginLocators


class LoginPage(BasePage):
    """Page Object de la page d'authentification.

    L'API publique utilise un vocabulaire métier compréhensible par un testeur
    fonctionnel. Les sélecteurs restent confinés au référentiel resources/locators.py.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page, "Authentification")
        self._username = page.locator(LoginLocators.USERNAME)
        self._password = page.locator(LoginLocators.PASSWORD)
        self._login_button = page.locator(LoginLocators.LOGIN_BUTTON)
        self._error = page.locator(LoginLocators.ERROR_MESSAGE)
        self._container = page.locator(LoginLocators.LOGIN_CONTAINER)

    def ouvrir_la_page_de_connexion(self) -> None:
        self.log.info(f"Ouverture de la page de connexion : {BASE_URL}")
        self.page.goto(BASE_URL, wait_until="domcontentloaded")
        self._attendre_visible(self._container, "formulaire de connexion")

    def saisir_le_nom_utilisateur(self, username: str) -> None:
        self.log.info(f"Saisie du nom utilisateur : {username!r}")
        self._attendre_saisissable(self._username, "champ nom utilisateur")
        self._username.fill(username)

    def saisir_le_mot_de_passe(self, password: str) -> None:
        self.log.info("Saisie du mot de passe : ******** (valeur masquée)")
        self._attendre_saisissable(self._password, "champ mot de passe")
        self._password.fill(password)

    def demander_la_connexion(self) -> None:
        self.log.info("Clic sur le bouton de connexion")
        self._attendre_cliquable(self._login_button, "bouton de connexion")
        self._login_button.click()

    def se_connecter_avec(self, username: str, password: str) -> None:
        self.log.info(f"Tentative de connexion pour {username!r}")
        self.saisir_le_nom_utilisateur(username)
        self.saisir_le_mot_de_passe(password)
        self.demander_la_connexion()

    def verifier_le_message_derreur(self, message_attendu: str) -> None:
        self.log.info(f"Vérification du message d'erreur attendu : {message_attendu!r}")
        self._attendre_visible(self._error, "message d'erreur")
        expect(self._error).to_have_text(message_attendu, timeout=self.timeout)

    def verifier_que_la_page_de_connexion_reste_affichee(self) -> None:
        self.log.info("Vérification que le formulaire de connexion reste affiché")
        expect(self._container).to_be_visible(timeout=self.timeout)
