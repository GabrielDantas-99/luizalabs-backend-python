from datetime import datetime

from pydantic import BaseModel

from src.models.transaction import TransactionType


class TransactionOut(BaseModel):
  """Dados de transação retornados pela API."""
  
  id: int
  account_id: int
  type: TransactionType
  amount: float
  timestamp: datetime

  model_config = {"from_attributes": True}