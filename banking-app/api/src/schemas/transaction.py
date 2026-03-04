from pydantic import BaseModel, Field

from src.models.transaction import TransactionType


class TransactionIn(BaseModel):
  """Informações necessárias para registrar um depósito ou saque."""
  account_id: int = Field(
    ..., 
    gt=0, 
    description="Identificação da conta para a qual a transação será realizada."
  )
  type: TransactionType = Field(..., description="Tipo de transação: 'depósito' ou 'saque'.")
  amount: float = Field(..., gt=0, description="Valor da transação. Deve ser estritamente positivo.")

  model_config = {
    "json_schema_extra": {
      "example": {
        "account_id": 1,
        "type": "deposit",
        "amount": 250.00,
      }
    }
  }