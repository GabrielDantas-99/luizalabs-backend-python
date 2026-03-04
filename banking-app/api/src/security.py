import time
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.config import settings
from src.views.auth import LoginOut

from src.views.auth import LoginOut

class TokenPayload:
  """Declarações JWT analisadas e validadas."""
  
  __slots__ = ("user_id", "exp", "jti")
  
  def __init__(self, user_id: int, exp: float, jti: str) -> None:
    self.user_id = user_id
    self.exp = exp
    self.jti = jti
    
def sign_jwt(user_id: int) -> LoginOut:
  """
  Emita um JWT assinado para o usuário especificado.

  As declarações seguem a RFC 7519:
    iss — emissor
    sub — sujeito (user_id)
    aud — público-alvo
    exp — tempo de expiração
    iat — emitido em
    nbf — não antes de
    jti — ID de token exclusivo (impede a repetição se armazenado)
  """
  now = time.time()
  
  payload = {
    "iss": "bank-api",
    "sub": user_id,
    "aud": "bank-api-client",
    "exp": now + settings.jwt_expire_minutes * 60,
    "iat": now,
    "nbf": now,
    "jti": uuid4().hex,
  }
  
  token = jwt.encode(
    payload, 
    settings.jwt_secret, 
    algorithm=settings.jwt_algorithm
  )
  
  return LoginOut(access_token=token)

def _decode_jwt(token: str) -> TokenPayload | None:
  """
  Decodifica e valida uma string JWT.
  Retorna um TokenPayload em caso de sucesso ou None se o token for inválido/expirado.
  Erros são intencionalmente ignorados aqui — os chamadores recebem uma resposta 401.
  """
  try:
    claims = jwt.decode(
      token,
      settings.jwt_secret,
      audience="bank-api-client",
      algorithms=[settings.jwt_algorithm]
    )
    return TokenPayload(
      user_id=int(claims["sub"]),
      exp=float(claims["exp"]),
      jti=str(claims["jti"])
    )
  except jwt.ExpiredSignatureError:
    return None
  except jwt.InvalidTokenError:
    return None
  
class JWTBearer(HTTPBearer):
  """
  Dependência de segurança do FastAPI que extrai e valida um JWT Bearer.
  Retorna um erro HTTP 401 para tokens ausentes, malformados ou expirados.
  Em caso de sucesso, retorna um TokenPayload acessível a dependências subsequentes.
  """
  def __init__(self) -> None:
    super().__init__(auto_error=False)

  async def __call__(self, request: Request) -> TokenPayload:  # type: ignore[override]
    credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)

    if not credentials:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authorization header missing or malformed.",
        headers={"WWW-Authenticate": "Bearer"},
      )

    if credentials.scheme.lower() != "bearer":
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication scheme. Expected 'Bearer'.",
        headers={"WWW-Authenticate": "Bearer"},
      )

    payload = _decode_jwt(credentials.credentials)
    if payload is None:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token is invalid or has expired.",
        headers={"WWW-Authenticate": "Bearer"},
      )

    return payload
  
_jwt_bearer = JWTBearer()

async def get_current_user(
  payload: Annotated[TokenPayload, Depends(_jwt_bearer)]
) -> TokenPayload:
  """
  Dependência FastAPI que resolve o usuário autenticado a partir do JWT.
  
  Uso em um roteador:
    @router.get("/me")
    async def me(user: Annotated[TokenPayload, Depends(get_current_user)]):
      return {"user_id": user.user_id}
  """
  return payload

login_required = get_current_user