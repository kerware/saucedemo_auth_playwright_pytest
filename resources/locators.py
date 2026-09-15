"""Référentiel UNIQUE des accesseurs utilisés par la suite E2E.

Aucun sélecteur ne doit être dupliqué dans les Page Objects ou dans les tests.
Priorité donnée aux attributs stables data-test. Un XPath est utilisé pour le titre
Products afin d'illustrer la prise en charge CSS / XPath dans le même référentiel.
"""


class LoginLocators:
    USERNAME = '[data-test="username"]'
    PASSWORD = '[data-test="password"]'
    LOGIN_BUTTON = '[data-test="login-button"]'
    ERROR_MESSAGE = '[data-test="error"]'
    LOGIN_CONTAINER = '[data-test="login-container"]'


class InventoryLocators:
    TITLE = "xpath=//span[@data-test='title' and normalize-space()='Products']"
    INVENTORY_LIST = '[data-test="inventory-list"]'
    PRODUCT_ITEM = '[data-test="inventory-item"]'
    PRODUCT_NAME = '[data-test="inventory-item-name"]'
    ADD_TO_CART_BUTTON = '[data-test^="add-to-cart-"]'
    SHOPPING_CART_LINK = '[data-test="shopping-cart-link"]'
    SHOPPING_CART_BADGE = '[data-test="shopping-cart-badge"]'


class CartLocators:
    TITLE = "xpath=//span[@data-test='title' and normalize-space()='Your Cart']"
    CART_LIST = '[data-test="cart-list"]'
    CART_ITEM = '[data-test="inventory-item"]'
    ITEM_NAME = '[data-test="inventory-item-name"]'
    REMOVE_BUTTON = '[data-test^="remove-"]'
