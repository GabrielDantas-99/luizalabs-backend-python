from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.schemas.transaction import TransactionIn
from src.security import TokenPayload, login_required
from src.services.transaction import TransactionService
from src.views.transaction import TransactionOut

router = APIRouter(prefix="/transactions")


def get_transaction_service() -> TransactionService:
  from src.database import database
  return TransactionService(db=database)


@router.post(
  "/",
  status_code=status.HTTP_201_CREATED,
  response_model=TransactionOut,
  summary="Crie uma transação",
  description=(
    "Registre um **depósito** ou **saque** em uma conta existente..\n\n"
    "- O valor deve ser estritamente positivo.\n"
    "- Os levantamentos são rejeitados se a conta não tiver saldo suficiente..\n"
    "- A atualização do saldo e o registro de transações são gravados atomicamente.."
  ),
  responses={
    201: {"description": "Transação registrada com sucesso."},
    404: {"description": "Conta não encontrada."},
    409: {"description": "Regra de negócio violada (ex.: saldo insuficiente)."},
  },
)
async def create_transaction(
  transaction: TransactionIn,
  _: Annotated[TokenPayload, Depends(login_required)] = None,
  service: TransactionService = Depends(get_transaction_service),
) -> TransactionOut:
  return await service.create(transaction)