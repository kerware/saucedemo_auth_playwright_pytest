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


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_FILE = PROJECT_ROOT / "data" / "authentication.csv"


def load_authentication_cases(path: Path = DEFAULT_DATA_FILE) -> list[AuthenticationCase]:
    """Charge les cas CSV avec ';' comme séparateur.

    Le module csv gère correctement les champs quotés : si un message contient une
    virgule (ou même un ';'), il suffit de conserver le champ entre guillemets.
    """
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
