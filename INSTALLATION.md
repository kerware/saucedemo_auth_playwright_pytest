# Note d'installation et d'exécution

## 1. Prérequis

Installer :

- Python **3.11 ou supérieur** ;
- `pip` ;
- un terminal PowerShell, CMD ou Bash ;
- une connexion Internet pour installer les dépendances et accéder à SauceDemo.

Vérification :

```powershell
python --version
python -m pip --version
```

## 2. Décompresser le projet

Décompresser `saucedemo_auth_playwright_pytest.zip`, puis ouvrir un terminal dans le dossier :

```powershell
cd saucedemo_auth_playwright_pytest
```

## 3. Créer un environnement virtuel

Sous Windows PowerShell :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Sous Linux / macOS :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Installer les dépendances Python

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Installer les moteurs Playwright

```powershell
playwright install
```

Sous Linux, si les dépendances système sont absentes :

```bash
playwright install --with-deps
```

## 6. Exécuter les tests

### Chromium uniquement

```powershell
pytest --browser chromium
```

ou :

```powershell
.\scripts\run_chromium.ps1
```

### Firefox uniquement

```powershell
pytest --browser firefox
```

### WebKit uniquement

```powershell
pytest --browser webkit
```

### Les trois navigateurs

```powershell
pytest --browser chromium --browser firefox --browser webkit
```

ou :

```powershell
.\scripts\run_all_browsers.ps1
```

## 7. Résultats produits

Après exécution :

- rapport HTML : `reports/report.html` ;
- captures d'écran des échecs : `reports/screenshots/` ;
- journal détaillé des actions : `logs/actions_YYYYMMDD_HHMMSS.log`.

Le journal masque volontairement la valeur du mot de passe.

## 8. Retry

Le fichier `pytest.ini` configure :

```text
--reruns=1
--reruns-delay=1
```

Un test en échec est donc rejoué **une fois** après une seconde. Pour désactiver ponctuellement le retry :

```powershell
pytest --reruns 0 --browser chromium
```

Pour utiliser deux retries :

```powershell
pytest --reruns 2 --browser chromium
```

## 9. Données de test CSV

Les cas se trouvent dans `data/authentication.csv`.

Le séparateur est le point-virgule `;`. Les messages sont entourés de guillemets. Le chargement utilise `csv.DictReader`, ce qui évite de casser une ligne si un message contient une virgule. Si un champ contient lui-même un `;`, il doit rester entre guillemets.

Colonnes :

```text
case_id;username;password;expected_result;expected_error
```

Valeurs attendues pour `expected_result` :

- `SUCCESS`
- `ERROR`

## 10. URL et timeout configurables

Par défaut :

- URL : `https://www.saucedemo.com`
- timeout : `15000` ms

Modification PowerShell :

```powershell
$env:SAUCEDEMO_BASE_URL = "https://www.saucedemo.com"
$env:E2E_TIMEOUT_MS = "20000"
pytest --browser chromium
```

La capture sur échec peut être désactivée :

```powershell
$env:SCREENSHOT_ON_FAILURE = "false"
pytest --browser chromium
```

## 11. Règle de maintenance des sélecteurs

Tous les accesseurs CSS / XPath sont centralisés dans :

```text
resources/locators.py
```

Il ne faut **jamais** ajouter un sélecteur directement dans un test ou dans un Page Object. En cas d'évolution de l'interface, ce fichier constitue le point unique de maintenance.
