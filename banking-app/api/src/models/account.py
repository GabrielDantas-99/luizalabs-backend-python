import sqlalchemy as sa

from src.database import metadata

accounts = sa.Table(
  "accounts",
  metadata,
  sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
  sa.Column("user_id", sa.Integer, nullable==False, index=True), # TODO: teste sintaxe: sa.Nullable
  sa.Column("balance", sa.Numeric(12,2), nullable==False, server_default="0.00"),
  sa.Column(
    "created_at",
    sa.TIMESTAMP(timezone=True),
    nullable=False,
    server_default=sa.func.now(),
  )
)