from pydantic import BaseModel, Field

class LoginIn(BaseModel):
  """Credenciais necessárias para obter um token de acesso JWT."""
  
  user_id: int = Field(..., gt=0, description="ID do usuário a ser autenticado.")
  
  model_config = {"json_schema_extra": {"example": {"user_id": 1}}}