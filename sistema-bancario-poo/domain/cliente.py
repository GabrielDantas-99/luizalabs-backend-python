from __future__ import annotations

from typing import TYPE_CHECKING

from .pessoa_fisica import PessoaFisica

if TYPE_CHECKING:
    from .conta import Conta
    from .transacao import Transacao


class Cliente(PessoaFisica):
    """Cliente do banco; pode possuir múltiplas contas."""

    def __init__(
        self, nome: str, data_nascimento: str, cpf: str, endereco: str
    ) -> None:
        super().__init__(nome, data_nascimento, cpf)
        self._endereco = endereco
        self._contas: list[Conta] = []

    @property
    def endereco(self) -> str:
        return self._endereco

    @property
    def contas(self) -> list[Conta]:
        """Retorna cópia defensiva da lista — impede mutação externa."""
        return list(self._contas)

    def adicionar_conta(self, conta: Conta) -> None:
        """Associa uma conta ao cliente."""
        if conta in self._contas:
            raise ValueError("Conta já está associada a este cliente.")
        self._contas.append(conta)

    def realizar_transacao(self, conta: Conta, transacao: Transacao) -> None:
        """Delega o registro da transação ao objeto Transacao (padrão Command)."""
        transacao.registrar(conta)

    def __repr__(self) -> str:
        return (
            f"Cliente(nome={self._nome!r}, cpf={self._cpf!r}, "
            f"contas={len(self._contas)})"
        )
