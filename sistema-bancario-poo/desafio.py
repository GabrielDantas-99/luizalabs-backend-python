from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class PessoaFisica:
  def __init__(
    self, nome: str, data_nascimento: str,cpf: str
  ) -> None:
    
    self.nome = nome
    self.data_nascimento = data_nascimento
    self.cpf = cpf

class Cliente(PessoaFisica):
  def __init__(self, nome: str, data_nascimento: str,cpf: str, endereco: str) -> None:
    super().__init__(nome, data_nascimento, cpf)
    self.endereco = endereco
    self.contas: list[Conta] = []
    
  def realizar_transacao(self, conta: Conta, transacao: Transacao) -> None:
    transacao.registrar(conta)
    
  def adicionar_conta(self, conta: Conta) -> None:
    self.contas.append(conta)


class Conta:
  def __init__(self, numero: str, cliente: Cliente) -> None:
    self._saldo = 0.0
    self._numero = numero
    self._agencia = "0001"
    self._cliente = cliente
    self._historico = Historico()
    
  @classmethod
  def nova_conta(cls, cliente: Cliente, numero: str):
    return cls(numero, cliente)
  
  @property
  def saldo(self) -> float:
    return self._saldo
  
  @property
  def numero(self) -> float:
    return self._saldo
  
  @property
  def agencia(self) -> str:
    return self._agencia
  
  @property
  def cliente(self) -> Cliente:
    return self._cliente
  
  @property
  def historico(self) -> Historico:
    return self._historico
  
  def sacar(self, valor: float) -> bool:
    saldo = self.saldo
    excedeu_saldo = valor > saldo
    
    if excedeu_saldo:
      raise ValueError("Operação falhou! Você não tem saldo suficiente.")
    elif valor > 0:
      self._saldo -= valor
      print("\n Saque realizado com sucesso!")
      return True
    else:
      print("\nOperação falhou! O valor informado é inválido!")
      
    return False
  
  def depositar(self, valor: float) -> bool:
    if valor > 0:
      self._saldo += valor
      print("\nDepósito realizado com sucesso!")
    else:
      raise ValueError("Operação falhou! O valor informado é inválido!")

    return True
  
class ContaCorrente(Conta):
  def __init__(
    self, numero: str, cliente: Cliente, limite=500, limite_saques=3
  ) -> None:
    super().__init__(numero, cliente)
    self.limite: int = limite
    self.limite_saques: int = limite_saques
    
  def sacar(self, valor: float) -> bool:
    numero_saques = len(
      [transacao for transacao in self.historico.transacoes 
       if transacao["tipo"] == Saque.__name__
      ]
    )
    
    excedeu_limite = valor > self.limite
    excedeu_saques = numero_saques >= self.limite_saques
    
    if excedeu_limite:
      print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
      print("Operação falhou! Número máximo de saques excedido.")
    else:
      return super().sacar(valor)
    
    return False
  
  def __str__(self) -> str:
    return f"""\
      Agência: \t {self.agencia}
      Cc:\t\t{self.numero}
      Titular:\t{self.cliente.nome}
    """

class Historico:
  def __init__(self) -> None:
    self._transacoes = []
    
  @property
  def transacoes(self) -> list[Transacao]:
    return self._transacoes
  
  def adicionar_transacao(self, transacao) -> None:
    self._transacoes.append(
      {
        "tipo": transacao.__class__.__name__,
        "valor": transacao.valor,
        "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s")
      }
    )

class Transacao(ABC):
  @property
  def valor(self):
    pass
  
  @classmethod
  def registrar(self, conta):
    pass
  
class Saque(Transacao):
  def __init__(self, valor):
    self._valor = valor
    
  @property
  def valor(self):
    return self._valor
  
  def registrar(self, conta: Conta) -> None:
    sucesso_transacao = conta.sacar(self.valor)
    
    if sucesso_transacao:
      conta.historico.adicionar_transacao(self)
    
class Deposito(Transacao):
  def __init__(self, valor) -> None:
    self._valor = valor
    
  @property
  def valor(self):
    return self._valor
  
  def registrar(self, conta: Conta):
    sucesso_transacao = conta.depositar(self.valor)
    
    if sucesso_transacao:
      conta.historico.adicionar_transacao(self)