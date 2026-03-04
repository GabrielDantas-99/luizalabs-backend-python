from fastapi import APIRouter, Depends, status

from src.database import database
from src.schemas.auth import LoginIn
from src.schemas.user import UserRegisterIn
from src.security import sign_jwt
from src.services.user import UserService
from src.views.auth import LoginOut
from src.views.user import UserOut

router = APIRouter(prefix="/auth")


def get_user_service() -> UserService:
    return UserService(db=database)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
    summary="Cadastre um novo usuário",
    description=(
        "Crie uma nova conta de usuário com nome, e-mail e senha. "
        "Após o cadastro, utilize o comando `POST /auth/login` para obter um token JWT."
    ),
    responses={
        201: {"description": "Usuário cadastrado com sucesso."},
        409: {"description": "E-mail já cadastrado."},
    },
)
async def register(
    data: UserRegisterIn,
    service: UserService = Depends(get_user_service),
) -> UserOut:
    return await service.register(data)


@router.post(
    "/login",
    response_model=LoginOut,
    summary="Autentique e obtenha um JWT.",
    description=(
        "Forneça seu e-mail e senha para receber um token de acesso JWT assinado. "
        "Inclua este token como `Authorization: Bearer <token>` em todos os endpoints protegidos.."
    ),
    responses={
        200: {"description": "JWT emitido com sucesso."},
        409: {"description": "E-mail ou senha inválidos."},
    },
)
async def login(
    data: LoginIn,
    service: UserService = Depends(get_user_service),
) -> LoginOut:
    user = await service.authenticate(email=data.email, password=data.password)
    return sign_jwt(user_id=user["id"])