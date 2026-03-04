from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
  """Dados do usuário retornados pela API. Nunca expõe o hash da senha."""

  id: int
  name: str
  email: EmailStr
  created_at: datetime

  model_config = {"from_attributes": True}