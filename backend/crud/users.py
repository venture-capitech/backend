# incl_path

from .. import models
from .. import schemas

from sqlalchemy.orm import Session

def get_user(db: Session, **kwargs):
    qry = db.query(models.User)
    
    for k, v in kwargs:
        if (k == "id"):
            qry = qry.filter(models.User.id == v)
        elif (k == "email"):
            qry = qry.filter(models.User.email == v)
            
    return qry.all()
    

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
