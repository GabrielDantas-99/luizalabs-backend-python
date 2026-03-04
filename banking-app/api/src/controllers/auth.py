from fastapi import APIRouter

from src.schemas.auth import LoginIn
from src.security import sign_jwt
from src.views.auth import LoginOut

router = APIRouter(prefix="/auth")

@router.post(
    "/login",
    response_model=LoginOut,
    summary="Autentique e obtenha um JWT.",
    description=("Forneça um `user_id` para receber um token de acesso JWT assinado."
    "Inclua este token como `Authorization: Bearer <token>` em todos os endpoints protegidos."
  ),
  responses={
    200: {"description": "JWT emitido com sucesso."},
  },
)
async def login(data: LoginIn) -> LoginOut:
  return sign_jwt(user_id=data.user_id)