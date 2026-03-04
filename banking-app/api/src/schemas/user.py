from pydantic import BaseModel, EmailStr, Field


class UserRegisterIn(BaseModel):
  """É necessário fornecer um Payload para cadastrar um novo usuário."""

  name: str = Field(..., min_length=2, max_length=100, description="Full name of the user.")
  email: EmailStr = Field(..., description="Endereço de e-mail exclusivo usado para fazer login.")
  password: str = Field(..., min_length=8, description="Senha (mínimo 8 caracteres).")

  model_config = {
    "json_schema_extra": {
      "example": {
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "password": "s3cr3tpass",
      }
    }
  }