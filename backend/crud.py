from backend import models, schemas
from sqlalchemy.orm import Session
import bcrypt

# By WM
# Password hashing and verification
def hash_password(password: str) -> str:
    # Generate a salt and hash the password
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Check if the given password matches the hashed password
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email=email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None
# End of WM

def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# get all users?
def get_users(db: Session, limit=None, skip: int = 0):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user