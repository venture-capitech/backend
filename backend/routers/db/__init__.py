# incl_path

from . import r_users
from . import r_accounts
from . import r_transactions

from ... import config

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

if (config.INC_DEBUG_ROUTES == 1):
    router.include_router(
        r_users.dbg_router,
        prefix="/debug/users",
        tags=["users"]
    )

    router.include_router(
        r_accounts.dbg_router,
        prefix="/debug/accounts",
        tags=["accounts"]
    )

    router.include_router(
        r_transactions.dbg_router,
        prefix="/debug/transactions",
        tags=["transactions"]
    )