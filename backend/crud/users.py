# incl_path

from .. import deps
from .. import models
from .. import schemas
from .. import utils


from typing import Annotated
from sqlalchemy.orm import Session
from enum import Enum, auto
from fastapi import Depends


class CONSTS(Enum):
    USER_EXISTS = auto()
    USER_CREATED = auto()
    USER_NOT_FOUND = auto()
    USER_VERIFIED = auto()
    USER_NOT_VERIFIED = auto()


def get_all_users(db: Session, **kwargs):
    qry = db.query(models.User)

    if ("id" in kwargs):
        qry = qry.filter(models.User.id == kwargs["id"])
    if ("email" in kwargs):
        qry = qry.filter(models.User.email == kwargs["email"])
    
    ret = qry.all()
    if (ret == []):
        return None
    return ret


def get_first_user(db: Session, **kwargs):
    qry = db.query(models.User)

    if ("id" in kwargs):
        qry = qry.filter(models.User.id == kwargs["id"])
    if ("email" in kwargs):
        qry = qry.filter(models.User.email == kwargs["email"])

    ret = qry.first()
    if (ret == []):
        return None
    return ret


def create_user(db: Session, user: schemas.UserCredentials):
    existing_usr = get_all_users(db, email=user.email)
    if (existing_usr is None):
        hashed_pw = utils.hash.hash(user.password)
        db_user = models.User(email=user.email, hashed_password=hashed_pw)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return CONSTS.USER_CREATED
    return CONSTS.USER_EXISTS


def verify_user(db: Session, user: schemas.UserCredentials):
    # todo refactor schema name
    existing_usr = get_first_user(db, email=user.email)
    if existing_usr is None:
        return CONSTS.USER_NOT_FOUND

    if utils.hash.verify_hash(user.password, existing_usr.hashed_password):
        return CONSTS.USER_VERIFIED    
    return CONSTS.USER_NOT_VERIFIED


# todo fix this
# async def get_current_user(db, token: Annotated[str, Depends(deps.oauth2_scheme)]):
#     user = get_first_user(db, token.user)
#     if not user:
#         return CONSTS.USER_NOT_VERIFIED
#     return user
