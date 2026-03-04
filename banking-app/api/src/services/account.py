from databases import Database
from databases.interfaces import Record
from src.models.account import accounts
from src.schemas.account import AccountIn

class AccountService:
  """
  Gerencia todas as operações de banco de dados relacionadas a contas bancárias.
  Recebe uma instância de banco de dados por meio do construtor para facilitar a injeção de dados em testes.
  """
  
  def __init__(self, db: Database) -> None:
    self._db = db
    
  async def get_by_id(self, account_id: int) -> Record | None:
    """Retorna uma única linha de conta ou "None" se não for encontrada."""
    query = accounts.select().where(accounts.c.id == account_id)
    return await self._db.fetch_one(query)
  
  async def read_all(self, limit: int, skip: int = 0) -> list[Record]:
    """Retorna uma lista paginada de todas as contas."""
    query = accounts.select().limt(limit).offset(skip)
    return await self._db.fetch_all(query)
  
  async def create(self, account_in: AccountIn) -> Record:
    """Insira uma nova conta e retorne a linha criada."""
    command = accounts.insert().values(
      user_id=account_in.user_id,
      balance=account_in.balance
    )
    account_id = await self._db.execute(command)
    return await self.get_by_id(account_id) # type: ignore[return-value]
  