from pydantic import BaseModel


class LoginOut(BaseModel):
    """Token de acesso JWT retornado após autenticação bem-sucedida."""

    access_token: str
    token_type: str = "bearer"