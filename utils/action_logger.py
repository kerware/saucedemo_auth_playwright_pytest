from __future__ import annotations

import logging


class ActionLogger:
    """Journal métier utilisé par les Page Objects.

    Les mots de passe ne sont jamais écrits dans les logs.
    """

    def __init__(self, component: str) -> None:
        self._logger = logging.getLogger("e2e.actions")
        self._component = component

    def info(self, message: str) -> None:
        self._logger.info("[%s] %s", self._component, message)

    def warning(self, message: str) -> None:
        self._logger.warning("[%s] %s", self._component, message)
