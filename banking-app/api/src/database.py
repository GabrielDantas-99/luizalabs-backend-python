import databases
import sqlalchemy as sa

from src.config import settings

# Conexão assíncrona com o banco de dados utilizada em toda a aplicação.
# Usa aiosqlite em desenvolvimento e asyncpg em produção.
database = databases.Database(settings.database_url)

# Registro de metadados — todas as definições de tabelas se vinculam aqui via sa.Table().
metadata = sa.MetaData()


def _sync_database_url() -> str:
  """
  Converte a URL assíncrona do banco de dados (DATABASE_URL) para seu equivalente síncrono para operações DDL.
  A função `create_engine()` é síncrona e não pode usar drivers assíncronos:
    sqlite+aiosqlite → sqlite
    postgresql+asyncpg → postgresql+psycopg2
  """
  url = settings.database_url
  return (
    url.replace("sqlite+aiosqlite", "sqlite")
        .replace("postgresql+asyncpg", "postgresql+psycopg2")
  )


def create_engine() -> sa.Engine:
  """
  Crie um mecanismo SQLAlchemy síncrono usado apenas para operações DDL (criação de tabelas, migrações Alembic). A E/S assíncrona usa o `database` acima.
  """
  sync_url = _sync_database_url()
  if settings.is_development:
    # O SQLite exige que check_same_thread=False seja configurado para acesso multithread.
    return sa.create_engine(sync_url, connect_args={"check_same_thread": False})
  return sa.create_engine(sync_url)


engine = create_engine()