# incl_path

from .. import models
from .. import schemas
from .. import utils

from sqlalchemy.orm import Session
from enum import Enum, auto


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


def create_user(db: Session, user: schemas.UserCreate):
    existing_usr = get_all_users(db, email=user.email)
    if (existing_usr is None):
        hashed_pw = utils.hash.hash(user.password)
        db_user = models.User(email=user.email, hashed_password=hashed_pw)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return CONSTS.USER_CREATED
    return CONSTS.USER_EXISTS


def verify_user(db: Session, user: schemas.UserCreate):
    # todo refactor schema name
    existing_usr = get_first_user(db, email=user.email)
    if existing_usr is None:
        return CONSTS.USER_NOT_FOUND

    if existing_usr.hashed_password == utils.hash.hash(user.password):
        return CONSTS.USER_VERIFIED
    
    return CONSTS.USER_NOT_VERIFIED
