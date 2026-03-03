from __future__ import annotations

from typing import TYPE_CHECKING

from .transacao import Transacao
from .excecoes import ValorInvalidoError

if TYPE_CHECKING:
    from .conta import Conta


class Deposito(Transacao):
    """Transação de crédito em conta."""

    def __init__(self, valor: float) -> None:
        if valor <= 0:
            raise ValorInvalidoError("O valor do depósito deve ser positivo.")
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: Conta) -> None:
        conta.depositar(self._valor)
        conta.historico.adicionar_transacao(self)

    def __repr__(self) -> str:
        return f"Deposito(valor={self._valor:.2f})"


class Saque(Transacao):
    """Transação de débito em conta."""

    def __init__(self, valor: float) -> None:
        if valor <= 0:
            raise ValorInvalidoError("O valor do saque deve ser positivo.")
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: Conta) -> None:
        conta.sacar(self._valor)
        conta.historico.adicionar_transacao(self)

    def __repr__(self) -> str:
        return f"Saque(valor={self._valor:.2f})"
