
import crud
import models
import schema
from database import SessionLocal, engine

from fastapi import Depends, FastAPI, HTTPException, Request, JSONResponse
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.api_route("/{path_name:path}", methods=["GET"])
async def catch_all_get(req: Request, path_name: str):
    
    raise HTTPException(status_code = 403, details = "User sent a GET Request")

    return JSONResponse(
        status_code = 403,
        content={"message": "yeah the server is working, just not for you"},
    )


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

