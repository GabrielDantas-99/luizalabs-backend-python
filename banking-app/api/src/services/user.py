import hashlib
import hmac

from databases import Database
from databases.interfaces import Record

from src.exceptions import BusinessError
from src.models.user import users
from src.schemas.user import UserRegisterIn


def _hash_password(password: str) -> str:
  """
  Gere um hash da senha em texto simples usando SHA-256.

  Para produção, substitua por bcrypt ou argon2 através da biblioteca 'passlib'.
  O uso do hashlib aqui evita adicionar uma nova dependência ao escopo do desafio.
  """
  return hashlib.sha256(password.encode()).hexdigest()


def _verify_password(plain: str, hashed: str) -> bool:
  """Comparar uma senha em texto simples com um hash armazenado (com segurança em relação ao tempo)."""
  return hmac.compare_digest(_hash_password(plain), hashed)


class UserService:
  def __init__(self, db: Database) -> None:
    self._db = db

  async def get_by_email(self, email: str) -> Record | None:
    """Retorna a linha do usuário por e-mail ou None caso não seja encontrada."""
    query = users.select().where(users.c.email == email)
    return await self._db.fetch_one(query)

  async def get_by_id(self, user_id: int) -> Record | None:
    """Retorna uma linha de usuário pelo ID, ou None se não for encontrada."""
    query = users.select().where(users.c.id == user_id)
    return await self._db.fetch_one(query)

  async def register(self, user_in: UserRegisterIn) -> Record:
    """
    Criar uma nova conta de usuário.

    Exceções:
      BusinessError: se o e-mail já estiver cadastrado.
    """
    existing = await self.get_by_email(user_in.email)
    if existing:
      raise BusinessError("E-mail already registered.")

    command = users.insert().values(
      name=user_in.name,
      email=user_in.email,
      password_hash=_hash_password(user_in.password),
    )
    user_id = await self._db.execute(command)
    return await self.get_by_id(user_id)  # type: ignore[return-value]

  async def authenticate(self, email: str, password: str) -> Record:
    """
    Verificar credenciais e retornar o registro do usuário.

    Exceções:
      BusinessError: se as credenciais forem inválidas.
    """
    user = await self.get_by_email(email)
    if not user or not _verify_password(password, user["password_hash"]):
      raise BusinessError("Invalid e-mail or password.")
    return user