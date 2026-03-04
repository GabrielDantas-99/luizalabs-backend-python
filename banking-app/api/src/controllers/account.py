from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from src.schemas.account import AccountIn
from src.security import TokenPayload, login_required
from src.services.account import AccountService
from src.services.transaction import TransactionService
from src.views.account import AccountOut
from src.views.transaction import TransactionOut

router = APIRouter(prefix="/accounts")


def get_account_service() -> AccountService:
    from src.database import database
    return AccountService(db=database)


def get_transaction_service() -> TransactionService:
    from src.database import database
    return TransactionService(db=database)


@router.get(
    "/",
    response_model=list[AccountOut],
    summary="List all accounts",
    description="Returns a paginated list of all bank accounts. Requires authentication.",
)
async def read_accounts(
    limit: Annotated[int, Query(ge=1, le=100, description="Max records to return.")] = 20,
    skip: Annotated[int, Query(ge=0, description="Number of records to skip.")] = 0,
    _: Annotated[TokenPayload, Depends(login_required)] = None,
    service: AccountService = Depends(get_account_service),
) -> list[AccountOut]:
    return await service.read_all(limit=limit, skip=skip)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=AccountOut,
    summary="Create an account",
    description="Creates a new bank account with an optional initial balance.",
    responses={
        201: {"description": "Account created successfully."},
    },
)
async def create_account(
    account: AccountIn,
    _: Annotated[TokenPayload, Depends(login_required)] = None,
    service: AccountService = Depends(get_account_service),
) -> AccountOut:
    return await service.create(account)


@router.get(
    "/{account_id}/transactions",
    response_model=list[TransactionOut],
    summary="Get account statement",
    description=(
        "Returns a paginated list of all transactions for the given account, "
        "ordered from most recent to oldest."
    ),
    responses={
        200: {"description": "Statement returned successfully."},
        404: {"description": "Account not found."},
    },
)
async def read_account_transactions(
    account_id: int,
    limit: Annotated[int, Query(ge=1, le=100, description="Max records to return.")] = 20,
    skip: Annotated[int, Query(ge=0, description="Number of records to skip.")] = 0,
    _: Annotated[TokenPayload, Depends(login_required)] = None,
    service: TransactionService = Depends(get_transaction_service),
) -> list[TransactionOut]:
    return await service.read_all(account_id=account_id, limit=limit, skip=skip)