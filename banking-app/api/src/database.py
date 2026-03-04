import databases
import sqlalchemy as sa

from src.config import settings

# Conexão assíncrona com o banco de dados utilizada em toda a aplicação.
# Usa aiosqlite em desenvolvimento e asyncpg em produção.
database = databases.Database(settings.database_url)

# Registro de metadados — todas as definições de tabelas se vinculam aqui via sa.Table().
metadata = sa.MetaData()

def create_engine() -> sa.Engine:
  """_summary_
  Cria um engine síncrono do SQLAlchemy usado apenas para operações DDL
  (criação de tabelas, migrações com Alembic). O I/O assíncrono utiliza `database` acima.
  Returns:
    sa.Engine: _description_
  """
  if settings.is_development:
    # O SQLite requer check_same_thread=False para acesso em múltiplas threads.
    return sa.create_engine(settings.database_url, connect_args={"check_same_thread": False})
  return sa.create_engine(settings.database_url)

engine = create_engine()
  