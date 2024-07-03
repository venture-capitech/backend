#incl_path

from . import database

from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
