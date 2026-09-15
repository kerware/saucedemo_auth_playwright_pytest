from __future__ import annotations

import os

BASE_URL = os.getenv("SAUCEDEMO_BASE_URL", "https://www.saucedemo.com").rstrip("/")
DEFAULT_TIMEOUT_MS = int(os.getenv("E2E_TIMEOUT_MS", "15000"))
SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
