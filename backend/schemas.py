# schemas.py

from pydantic import BaseModel
from typing import List, Optional

# User schemas
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    accounts: List['Account']  # List of Account objects

    class Config:
        orm_mode = True

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
