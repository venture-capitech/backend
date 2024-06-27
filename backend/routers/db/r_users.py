# incl_path

from ... import schemas
from ... import db_crud
from ... import database
from ... import deps

from fastapi import (
    APIRouter, HTTPException, Depends
)
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: database.Session = Depends(deps.get_db)):
    db_user = db_crud.get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_crud.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: database.Session = Depends(deps.get_db)):
    db_user = db_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/all", response_model=list[schemas.User])
async def read_all_users(skip: int = 0, limit=None, db: Session = Depends(deps.get_db)):
    users = db_crud.get_users(db, skip=skip, limit=limit)
    return users