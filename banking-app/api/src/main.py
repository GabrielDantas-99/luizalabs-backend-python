from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import settings
from src.controllers import account, auth, transaction
from src.database import database, engine, metadata
from src.exceptions import AccountNotFoundError, BusinessError

# ── Ciclo de vida (Lifespan) ───────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
  # Criar todas as tabelas na inicialização (idempotente — ignora tabelas existentes).
  # Em produção, prefira migrações Alembic em vez de metadata.create_all().
  metadata.create_all(engine)
  await database.connect()
  yield
  await database.disconnect()

# ── Metadados OpenAPI ──────────────────────────────────────────────────────────

_tags_metadata = [
  {
    "name": "auth",
    "description": "Obtenha um token de acesso JWT para autenticar solicitações subsequentes.",
  },
  {
    "name": "accounts",
    "description": "Criar contas e obter extratos de contas.",
  },
  {
    "name": "transactions",
    "description": "Registre depósitos e saques em contas existentes.",
  },
]

# ── Fábrica da aplicação ───────────────────────────────────────────────────────

app = FastAPI(
  title="Bank API",
  version="1.0.0",
  summary="Microsserviço bancário assíncrono para depósitos, saques e extratos de conta.",
  description="""
  ## Bank API

  Uma API bancária RESTful assíncrona construída com **FastAPI**.

  ### Fluxo
  1. **Autentique-se** via `POST /auth/login` para receber um token Bearer.
  2. **Crie uma conta** via `POST /accounts/`.
  3. **Deposite ou saque** via `POST /transactions/`.
  4. **Visualize o extrato** via `GET /accounts/{account_id}/transactions`.

  ### Autenticação
  Todos os endpoints `/accounts` e `/transactions` exigem:
  ```
  Authorization: Bearer <seu_token>
  ```
  """,
  openapi_tags=_tags_metadata,
  redoc_url="/redoc",
  lifespan=lifespan,
)

# ── Middleware ─────────────────────────────────────────────────────────────────

app.add_middleware(
  CORSMiddleware,
  allow_origins=settings.cors_origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# ── Rotas ──────────────────────────────────────────────────────────────────────

app.include_router(auth.router, tags=["auth"])
app.include_router(account.router, tags=["accounts"])
app.include_router(transaction.router, tags=["transactions"])

# ── Manipuladores de exceção ───────────────────────────────────────────────────

@app.exception_handler(AccountNotFoundError)
async def account_not_found_handler(request: Request, exc: AccountNotFoundError) -> JSONResponse:
  return JSONResponse(
    status_code=status.HTTP_404_NOT_FOUND,
    content={"detail": "Conta não encontrada."},
  )


@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError) -> JSONResponse:
  return JSONResponse(
    status_code=status.HTTP_409_CONFLICT,
    content={"detail": str(exc)},
  )