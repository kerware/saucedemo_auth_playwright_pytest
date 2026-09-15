# SauceDemo — Non-régression de l'authentification

Projet E2E limité à la fonctionnalité **Authentification** de SauceDemo.

## Stack

- Python 3.11+
- Pytest
- Playwright Python
- pytest-playwright
- pytest-html
- pytest-rerunfailures

## Principes d'architecture

- **Page Object Model** : `pages/login_page.py`, `pages/inventory_page.py` et `pages/cart_page.py`.
- **Référentiel unique de sélecteurs** : `resources/locators.py`.
- **API métier des pages** : méthodes en vocabulaire fonctionnel, sans sélecteur dans les tests.
- **Attentes explicites** : visibilité / éditabilité / activation avant les actions sensibles.
- **Données externes CSV** : `data/authentication.csv` et `data/cart.csv`, séparateur `;`, lecture avec `csv.DictReader`.
- **Journal des actions** : `logs/actions_YYYYMMDD_HHMMSS.log`.
- **Captures sur échec** : `reports/screenshots/`, attachées au rapport HTML lorsque possible.
- **Rapport HTML** : `reports/report.html`.
- **Multi-navigateur** : Chromium, Firefox, WebKit.
- **Retry** : 1 nouvelle tentative automatique par défaut, après 1 seconde.

## Couverture de non-régression

Le jeu de données couvre :

- connexion réussie avec `standard_user` ;
- connexion réussie avec les autres comptes acceptés (`problem_user`, `performance_glitch_user`, `error_user`, `visual_user`) ;
- rejet du compte `locked_out_user` ;
- rejet d'un mauvais mot de passe ;
- contrôle du nom utilisateur obligatoire ;
- contrôle du mot de passe obligatoire.

La couverture inclut désormais l'ajout d'un produit, l'ajout de plusieurs produits et la suppression d'un produit dans le panier. Aucun scénario checkout ou logout n'est testé.

## Lancement rapide

```bash
python -m venv .venv
```

Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install
pytest --browser chromium
```

Tous les navigateurs :

```powershell
pytest --browser chromium --browser firefox --browser webkit
```

Voir `INSTALLATION.md` pour les instructions détaillées.
