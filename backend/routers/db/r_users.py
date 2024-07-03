# incl_path

from ... import crud
from ... import schemas
from ... import database
from ... import deps

from fastapi import (
    APIRouter, HTTPException, Depends, status
)
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    create_user_status = crud.users.create_user(db, user=user)
    if (create_user_status == crud.users.CONSTS.USER_EXISTS):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    elif (create_user_status == crud.users.CONSTS.USER_CREATED):
        return {"message": "User Created"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown Error")


@router.get("/get/all", status_code=status.HTTP_200_OK)
async def read_all_users(db: Session = Depends(deps.get_db)):
    users = crud.users.get_all_users(db)
    return users


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

@router.post("/verify", status_code=status.HTTP_201_CREATED)
async def verify_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    verify_user_status = crud.users.verify_user(db, user=user)
    if (verify_user_status == crud.users.CONSTS.USER_NOT_FOUND):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    elif (verify_user_status == crud.users.CONSTS.USER_NOT_VERIFIED):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Credentials")
    elif (verify_user_status == crud.users.CONSTS.USER_VERIFIED):
        return {"message": "ok"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown Error")
