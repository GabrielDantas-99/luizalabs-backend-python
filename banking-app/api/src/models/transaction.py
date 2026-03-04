from enum import StrEnum

import sqlalchemy as sa

from src.database import metadata

class TransactionType(StrEnum):
  """_summary_
  Tipos de transação suportados.
  Utilizando StrEnum para que os valores sejam serializados naturalmente como strings em JSON e no banco de dados.
  Args:
    StrEnum (_type_): _description_
  """
  DEPOIST = "deposit"
  WITHDRAWAL = "withdrawal"
  
transactions = sa.Table(
  "transactions",
  metadata,
  sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
  sa.Column(
    "account_id",
    sa.Integer,
    sa.ForeignKey("accounts.id", ondelete="CASCADE"),
    nullable=False,
    index=True,
  ),
  sa.Column(
    "type",
    sa.Enum(TransactionType, name="transaction_type"),
    nullable=False,
  ),
  # Somente valores positivos — aplicado na camada de aplicação via Pydantic PositiveFloat.
  sa.Column("amount", sa.Numeric(12,2), nullable=False),
  sa.Column(
    "timestamp",
    sa.TIMESTAMP(timezone=True),
    nullable=False,
    server_default=sa.func.now()
  )
)