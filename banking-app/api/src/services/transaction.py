from databases import Database
from databases.interfaces import Record

from src.exceptions import AccountNotFoundError, BusinessError
from src.models.account import accounts
from src.models.transaction import TransactionType, transactions
from src.schemas.transaction import TransactionIn


class TransactionService:
  """
  Gerencia operações de depósito e saque com validação completa de regras de negócio.
  Todas as gravações são encapsuladas em uma transação de banco de dados para garantir a consistência:
  se a atualização do saldo falhar após a inserção da linha da transação (ou vice-versa), toda a operação é revertida.
  """

  def __init__(self, db: Database) -> None:
    self._db = db

  async def read_all(self, account_id: int, limit: int, skip: int = 0) -> list[Record]:
    """Retorna uma lista paginada de transações para uma determinada conta (extrato)."""
    query = (
      transactions.select()
      .where(transactions.c.account_id == account_id)
      .order_by(transactions.c.timestamp.desc())
      .limit(limit)
      .offset(skip)
    )
    return await self._db.fetch_all(query)

  async def create(self, transaction_in: TransactionIn) -> Record:
    """
    Registre um depósito ou saque e atualize o saldo da conta atomicamente.

    Exceções:
      AccountNotFoundError: se o ID da conta não existir.
      BusinessError: se um saque deixar o saldo negativo.
    """
    async with self._db.transaction():
      account = await self._fetch_account(transaction_in.account_id)
      new_balance = self._calculate_new_balance(account, transaction_in)

      transaction_id = await self._insert_transaction(transaction_in)
      await self._update_balance(transaction_in.account_id, new_balance)

    query = transactions.select().where(transactions.c.id == transaction_id)
    return await self._db.fetch_one(query)  # type: ignore[return-value]

  async def _fetch_account(self, account_id: int) -> Record:
      query = accounts.select().where(accounts.c.id == account_id)
      account = await self._db.fetch_one(query)
      if account is None:
        raise AccountNotFoundError()
      return account

  def _calculate_new_balance(self, account: Record, transaction_in: TransactionIn) -> float:
    """
    Calcula o saldo após a aplicação da transação.

    Gera um erro BusinessError se um saque resultar em saldo negativo.
    """
    current_balance = float(account["balance"])

    if transaction_in.type == TransactionType.WITHDRAWAL:
      new_balance = current_balance - transaction_in.amount
      if new_balance < 0:
        raise BusinessError(
          f"Insufficient balance. Available: {current_balance:.2f}, "
          f"requested: {transaction_in.amount:.2f}."
        )
      return new_balance

    return current_balance + transaction_in.amount

  async def _insert_transaction(self, transaction_in: TransactionIn) -> int:
    command = transactions.insert().values(
      account_id=transaction_in.account_id,
      type=transaction_in.type,
      amount=transaction_in.amount,
    )
    return await self._db.execute(command)

  async def _update_balance(self, account_id: int, new_balance: float) -> None:
    command = (
      accounts.update()
      .where(accounts.c.id == account_id)
      .values(balance=new_balance)
    )
    await self._db.execute(command)