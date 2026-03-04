import sqlalchemy as sa

from src.database import metadata

users = sa.Table(
  "users",
  metadata,
  sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
  sa.Column("name", sa.String(100), nullable=False),
  sa.Column("email", sa.String(255), nullable=False, unique=True, index=True),
  sa.Column("password_hash", sa.String(255), nullable=False),
  sa.Column(
    "created_at",
    sa.TIMESTAMP(timezone=True),
    nullable=False,
    server_default=sa.func.now(),
  ),
)