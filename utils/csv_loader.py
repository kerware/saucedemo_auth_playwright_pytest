from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AuthenticationCase:
    case_id: str
    username: str
    password: str
    expected_result: str
    expected_error: str

    @property
    def should_succeed(self) -> bool:
        return self.expected_result.upper() == "SUCCESS"


@dataclass(frozen=True)
class CartProductCase:
    case_id: str
    product_name: str


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_FILE = PROJECT_ROOT / "data" / "authentication.csv"
DEFAULT_CART_DATA_FILE = PROJECT_ROOT / "data" / "cart.csv"


def load_authentication_cases(path: Path = DEFAULT_DATA_FILE) -> list[AuthenticationCase]:
    """Charge les cas CSV avec ';' comme séparateur."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";", quotechar='"')
        required = {"case_id", "username", "password", "expected_result", "expected_error"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Colonnes CSV manquantes : {sorted(missing)}")

        cases = [
            AuthenticationCase(
                case_id=(row["case_id"] or "").strip(),
                username=row["username"] or "",
                password=row["password"] or "",
                expected_result=(row["expected_result"] or "").strip(),
                expected_error=row["expected_error"] or "",
            )
            for row in reader
        ]

    if not cases:
        raise ValueError(f"Aucun cas de test trouvé dans {path}")
    return cases


def load_cart_products(path: Path = DEFAULT_CART_DATA_FILE) -> list[CartProductCase]:
    """Charge les produits panier depuis un CSV séparé par ';'."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";", quotechar='"')
        required = {"case_id", "product_name"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Colonnes CSV manquantes : {sorted(missing)}")

        products = [
            CartProductCase(
                case_id=(row["case_id"] or "").strip(),
                product_name=(row["product_name"] or "").strip(),
            )
            for row in reader
        ]

    if not products or any(not product.product_name for product in products):
        raise ValueError(f"Aucun produit panier valide trouvé dans {path}")
    return products
