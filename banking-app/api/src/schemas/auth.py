from pydantic import BaseModel, EmailStr, Field

class LoginIn(BaseModel):
  """Credenciais necessárias para obter um token de acesso JWT."""
  
  email: EmailStr = Field(..., description="Endereço de e-mail utilizado durante o cadastro.")
  password: str = Field(..., min_length=8, description="Senha da conta.")

  model_config = {
    "json_schema_extra": {
      "example": {
        "email": "ada@example.com",
        "password": "s3cr3tpass",
      }
    }
  }