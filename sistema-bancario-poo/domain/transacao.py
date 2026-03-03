from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .conta import Conta


class Transacao(ABC):
    """Interface para todas as transações bancárias (padrão Command)."""

    @property
    @abstractmethod
    def valor(self) -> float:
        """Valor monetário da transação."""

    @abstractmethod
    def registrar(self, conta: Conta) -> None:
        """Executa e persiste a transação no histórico da conta."""
