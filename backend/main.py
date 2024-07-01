from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import crud, models, schemas
from backend.database import SessionLocal, engine

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency for OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Utility function to simulate token verification
def verify_token(token: str):
    # In a real-world application, you would decode and verify the token here
    return {"sub": "user@example.com"}  # Example payload

# GET user
@app.get("/user/{user_id}", response_model=schemas.User)
async def read_user(
    user_id: int, 
    db: Session = Depends(get_db)
    ):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# POST user
@app.post("/user/", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db)
    ):
    db_user = crud.get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# POST login
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Create and return a token here (simulated in this example)
    return {"access_token": "token", "token_type": "bearer"}

# POST transaction
@app.post("/transaction/")
async def create_transaction(
    from_account_id: int, 
    to_account_id: int, 
    amount: int,
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
    ):
    # Verify token and extract user info (for simplicity, simulated here)
    user_info = verify_token(token)
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Add transaction logic
    from_account = db.query(models.Account).filter(models.Account.id == from_account_id).first()
    to_account = db.query(models.Account).filter(models.Account.id == to_account_id).first()

    if not from_account or not to_account:
        raise HTTPException(status_code=404, detail="Account not found")

    if from_account.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Create transaction
    transaction = models.Transaction(
        amount=amount,
        from_account_id=from_account_id,
        to_account_id=to_account_id
    )
    db.add(transaction)

    # Update balances
    from_account.balance -= amount
    to_account.balance += amount

    db.commit()
    db.refresh(transaction)

    return transaction
