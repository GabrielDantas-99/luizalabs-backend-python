from datetime import datetime

from pydantic import BaseModel


class AccountOut(BaseModel):
  """Dados da conta retornados pela API."""

  id: int
  user_id: int
  balance: float
  created_at: datetime

  model_config = {"from_attributes": True}