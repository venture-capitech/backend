# incl_path

from . import r_users
from . import r_accounts
from . import r_transactions

from fastapi import APIRouter

router = APIRouter()

router.include_router(
    r_users.router,
    prefix="/users",
    tags=["users"]
)

router.include_router(
    r_accounts.router,
    prefix="/accounts",
    tags=["accounts"]
)

router.include_router(
    r_transactions.router,
    prefix="/transactions",
    tags=["transactions"]
)
