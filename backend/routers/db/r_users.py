# incl_path

from ... import crud
from ... import models
from ... import schemas
from ... import database
from ... import deps

from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import (
    APIRouter, HTTPException, Depends, status
)
from sqlalchemy.orm import Session

router = APIRouter()
dbg_router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCredentials, db: Session = Depends(deps.get_db)):
    create_user_status = crud.users.create_user(db, user=user)
    if (create_user_status == crud.users.CONSTS.USER_EXISTS):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    elif (create_user_status == crud.users.CONSTS.USER_CREATED):
        return {"message": "User Created"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown Error")


@router.get("/get/email/{user_email}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def read_user_by_email(user_email: str, db: Session = Depends(deps.get_db)):
    db_user = crud.users.get_first_user(db, email=user_email)
    if db_user is crud.users.CONSTS.USER_NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.get("/get/id/{user_id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def read_user_by_id(user_id: int, db: Session = Depends(deps.get_db)):
    db_user = crud.users.get_first_user(db, id=user_id)
    if db_user is crud.users.CONSTS.USER_NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


# todo fix this
# @router.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(deps.get_db)):
#     # use struct to populate
#     user = schemas.UserCredentials
#     user.email = form_data.username
#     user.password = form_data.password
#     verify_user_status = crud.users.verify_user(db, user=user)
#     if (verify_user_status == crud.users.CONSTS.USER_NOT_FOUND):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     elif (verify_user_status == crud.users.CONSTS.USER_NOT_VERIFIED):
#         return HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     elif (verify_user_status == crud.users.CONSTS.USER_VERIFIED):
#         return {"access_token": user.email, "token_type": "bearer"}
#     else:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown Error")


@dbg_router.get("/get/all", response_model=list[schemas.User], status_code=status.HTTP_200_OK)
async def read_all_users(db: Session = Depends(deps.get_db)):
    users = crud.users.get_all_users(db)
    return users


# todo fix this
# @dbg_router.get("/get/me")
# async def read_users_me(db: Session = Depends(deps.get_db)):
#     current_user = crud.users.get_current_user(db)
#     if (current_user == crud.users.CONSTS.USER_NOT_VERIFIED):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return current_user


@dbg_router.post("/verify", status_code=status.HTTP_202_ACCEPTED)
async def verify_user(user: schemas.UserCredentials, db: Session = Depends(deps.get_db)):
    verify_user_status = crud.users.verify_user(db, user=user)
    if (verify_user_status == crud.users.CONSTS.USER_NOT_FOUND):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    elif (verify_user_status == crud.users.CONSTS.USER_NOT_VERIFIED):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Credentials")
    elif (verify_user_status == crud.users.CONSTS.USER_VERIFIED):
        return {"message": "User Verified"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown Error")
