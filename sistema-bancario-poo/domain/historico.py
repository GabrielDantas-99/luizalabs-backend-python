from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .transacao import Transacao


class Historico:
    """Mantém o registro de todas as transações de uma conta."""

    def __init__(self) -> None:
        self._transacoes: list[dict] = []

    @property
    def transacoes(self) -> list[dict]:
        """Retorna cópia defensiva do histórico."""
        return list(self._transacoes)

    def adicionar_transacao(self, transacao: Transacao) -> None:
        """Registra um snapshot da transação com data/hora."""
        self._transacoes.append(
            {
                "tipo": type(transacao).__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def __repr__(self) -> str:
        return f"Historico(transacoes={len(self._transacoes)})"
