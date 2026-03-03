from __future__ import annotations

import textwrap
from typing import TYPE_CHECKING

from .historico import Historico
from .excecoes import SaldoInsuficienteError, ValorInvalidoError
from .excecoes import LimiteSaqueExcedidoError, NumeroSaquesExcedidoError

if TYPE_CHECKING:
    from .cliente import Cliente
    from .transacao import Saque


class Conta:
    """Conta bancária base com operações de saque e depósito."""

    AGENCIA_PADRAO = "0001"

    def __init__(self, numero: str, cliente: Cliente) -> None:
        self._saldo: float = 0.0
        self._numero: str = numero
        self._agencia: str = self.AGENCIA_PADRAO
        self._cliente: Cliente = cliente
        self._historico: Historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: str) -> Conta:
        """Cria e retorna uma nova instância de conta."""
        return cls(numero, cliente)

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> str:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    def sacar(self, valor: float) -> None:
        """Debita `valor` do saldo. Lança exceção em caso de erro."""
        if valor <= 0:
            raise ValorInvalidoError("O valor do saque deve ser positivo.")
        if valor > self._saldo:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente. Saldo atual: R$ {self._saldo:.2f}."
            )
        self._saldo -= valor
        print("\nSaque realizado com sucesso!")

    def depositar(self, valor: float) -> None:
        """Credita `valor` no saldo. Lança exceção em caso de erro."""
        if valor <= 0:
            raise ValorInvalidoError("O valor do depósito deve ser positivo.")
        self._saldo += valor
        print("\nDepósito realizado com sucesso!")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"agencia={self._agencia!r}, numero={self._numero!r}, "
            f"saldo={self._saldo:.2f})"
        )


class ContaCorrente(Conta):
    """Conta corrente com limite de valor por saque e limite de saques diários."""

    LIMITE_PADRAO = 500.0
    LIMITE_SAQUES_PADRAO = 3

    def __init__(
        self,
        numero: str,
        cliente: Cliente,
        limite: float = LIMITE_PADRAO,
        limite_saques: int = LIMITE_SAQUES_PADRAO,
    ) -> None:
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self) -> float:
        return self._limite

    @property
    def limite_saques(self) -> int:
        return self._limite_saques

    def sacar(self, valor: float) -> None:
        """Sobrescreve o saque adicionando verificações de limite e quantidade."""
        numero_saques = sum(
            1 for t in self._historico.transacoes if t["tipo"] == "Saque"
        )

        if valor > self._limite:
            raise LimiteSaqueExcedidoError(
                f"Valor excede o limite de R$ {self._limite:.2f} por saque."
            )
        if numero_saques >= self._limite_saques:
            raise NumeroSaquesExcedidoError(
                f"Limite de {self._limite_saques} saques diários atingido."
            )

        super().sacar(valor)

    def __str__(self) -> str:
        return textwrap.dedent(f"""\
            Agência:  {self._agencia}
            C/C:      {self._numero}
            Titular:  {self._cliente.nome}
            Saldo:    R$ {self._saldo:.2f}
        """)
