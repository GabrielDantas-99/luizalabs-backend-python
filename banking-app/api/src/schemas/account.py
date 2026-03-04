from pydantic import BaseModel, Field

class AccountIn(BaseModel):
  """Informações necessárias para criar uma nova conta bancária."""
  
  user_id: int = Field(..., gt=0, description="ID do usuário titular da conta.")
  balance: float = Field(
    default=0.0,
    ge=0,
    description="Saldo inicial. Deve ser zero ou positivo."
  )
  
  model_config = {"json_schema_extra": {"example": {"user_id": 1, "balance": 1000.00}}}