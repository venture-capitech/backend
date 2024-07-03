# schema.py

from pydantic import BaseModel
from typing import Optional, List
from sqlmodel import Field, SQLModel
from sqlalchemy.orm import relationship

# from backend.models import Account 

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    accounts: List['Account']

    class Config:
        orm_mode = True

# # Using SQLMOdel? not too sure how this works yet
# class User(SQLModel, table=True):

#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     email: str
#     hashed_password: str
#     is_active: bool

#     accounts = relationship("Account", back_populates="user")

# By WM
# Account schemas
class AccountBase(BaseModel):
    entityType: str  # Use string for Enum representation
    balance: int

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    owner: int  # ID of the user who owns the account

    class Config:
        orm_mode = True

# Transaction schemas
class TransactionBase(BaseModel):
    amount: int
    from_account_id: int
    to_account_id: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True