from __future__ import annotations

import textwrap
from typing import Optional

from domain.cliente import Cliente
from domain.conta import Conta, ContaCorrente
from domain.operacoes import Deposito, Saque
from domain.excecoes import (
    ValorInvalidoError,
    SaldoInsuficienteError,
    LimiteSaqueExcedidoError,
    NumeroSaquesExcedidoError,
)


class Banco:
    """
    Controlador principal da aplicação.
    Concentra o estado global (clientes e contas) e orquestra a UI de texto.
    """

    _CPF_PROMPT = "Informe o CPF do cliente: "

    def __init__(self) -> None:
        self._clientes: list[Cliente] = []
        self._contas: list[Conta] = []
        self._proximo_numero_conta: int = 1

    # ── Helpers internos ────────────────────────────────────

    def _filtrar_cliente(self, cpf: str) -> Optional[Cliente]:
        """Retorna o cliente com o CPF informado ou None."""
        return next((c for c in self._clientes if c.cpf == cpf), None)

    def _selecionar_conta(self, cliente: Cliente) -> Optional[Conta]:
        """Retorna a primeira conta do cliente, ou None se não houver."""
        contas = cliente.contas
        if not contas:
            print("\nCliente não possui conta cadastrada.")
            return None
        return contas[0]

    def _obter_cliente_e_conta(self) -> tuple[Optional[Cliente], Optional[Conta]]:
        """Fluxo reutilizável: lê CPF, valida cliente e retorna (cliente, conta)."""
        cpf = input(self._CPF_PROMPT)
        cliente = self._filtrar_cliente(cpf)
        if not cliente:
            print("\nCliente não encontrado.")
            return None, None
        conta = self._selecionar_conta(cliente)
        return cliente, conta

    # ── Operações de negócio ────────────────────────────────

    def depositar(self) -> None:
        cliente, conta = self._obter_cliente_e_conta()
        if not conta:
            return
        try:
            valor = float(input("Informe o valor do depósito: "))
            cliente.realizar_transacao(conta, Deposito(valor))
        except (ValorInvalidoError, ValueError) as e:
            print(f"\nOperação falhou! {e}")

    def sacar(self) -> None:
        cliente, conta = self._obter_cliente_e_conta()
        if not conta:
            return
        try:
            valor = float(input("Informe o valor do saque: "))
            cliente.realizar_transacao(conta, Saque(valor))
        except (
            ValorInvalidoError,
            SaldoInsuficienteError,
            LimiteSaqueExcedidoError,
            NumeroSaquesExcedidoError,
            ValueError,
        ) as e:
            print(f"\nOperação falhou! {e}")

    def exibir_extrato(self) -> None:
        _, conta = self._obter_cliente_e_conta()
        if not conta:
            return

        print("\n" + "=" * 42)
        print("          EXTRATO BANCÁRIO")
        print("=" * 42)

        transacoes = conta.historico.transacoes
        if not transacoes:
            print("  Nenhuma transação realizada.")
        else:
            for t in transacoes:
                sinal = "+" if t["tipo"] == Deposito.__name__ else "-"
                print(f"  {t['data']}  {t['tipo']:<10} {sinal}R$ {t['valor']:>9.2f}")

        print("-" * 42)
        print(f"  Saldo atual:             R$ {conta.saldo:>9.2f}")
        print("=" * 42)

    def criar_cliente(self) -> None:
        cpf = input(self._CPF_PROMPT)
        if self._filtrar_cliente(cpf):
            print("\nJá existe um cliente cadastrado com esse CPF.")
            return

        nome = input("Nome completo: ")
        data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
        endereco = input("Endereço (logradouro, bairro, cidade/UF): ")

        cliente = Cliente(
            nome=nome,
            data_nascimento=data_nascimento,
            cpf=cpf,
            endereco=endereco,
        )
        self._clientes.append(cliente)
        print("\nCliente cadastrado com sucesso!")

    def criar_conta(self) -> None:
        cpf = input(self._CPF_PROMPT)
        cliente = self._filtrar_cliente(cpf)
        if not cliente:
            print("\nCliente não encontrado. Cadastre-o antes de abrir uma conta.")
            return

        numero = str(self._proximo_numero_conta).zfill(6)
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero)

        self._contas.append(conta)
        cliente.adicionar_conta(conta)
        self._proximo_numero_conta += 1

        print(f"\nConta corrente nº {numero} criada com sucesso!")

    def listar_contas(self) -> None:
        if not self._contas:
            print("\nNenhuma conta cadastrada.")
            return
        for conta in self._contas:
            print("=" * 50)
            print(str(conta))

    # ── Loop principal ──────────────────────────────────────

    def executar(self) -> None:
        """Inicia o loop de menu da aplicação."""
        acoes: dict[str, callable] = {
            "d":  self.depositar,
            "s":  self.sacar,
            "e":  self.exibir_extrato,
            "nu": self.criar_cliente,
            "nc": self.criar_conta,
            "lc": self.listar_contas,
        }

        while True:
            opcao = self._menu()
            if opcao == "q":
                print("\nAté logo!")
                break
            acao = acoes.get(opcao)
            if acao:
                acao()
            else:
                print("\nOpção inválida. Tente novamente.")

    @staticmethod
    def _menu() -> str:
        opcoes = """\n
        ========== Menu ==========
        [d]   Depositar
        [s]   Sacar
        [e]   Extrato
        [nc]  Nova Conta
        [lc]  Listar Contas
        [nu]  Novo Usuário
        [q]   Sair
        => """
        return input(textwrap.dedent(opcoes)).strip().lower()
