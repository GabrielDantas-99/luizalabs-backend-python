class AppError(Exception):
  """Classe base para todos os erros a nível de aplicação."""


class AccountNotFoundError(AppError):
  """Lançado quando uma conta solicitada não existe no banco de dados."""


class BusinessError(AppError):
  """
  Lançado quando uma regra de negócio é violada.

  Exemplos:
    - O valor do saque excede o saldo disponível.
    - Valores de transação negativos ou iguais a zero (devem ser capturados primeiro pelo Pydantic).

  Sempre forneça uma mensagem descritiva:
    raise BusinessError("Saldo insuficiente para concluir este saque.")
  """