# incl_path

from . import db

from fastapi import APIRouter

router = APIRouter()

router.include_router(
    db.router,
    prefix=""
)
