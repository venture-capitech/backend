# schema.py

from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCredentials(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    accounts: list

    class Config:
        orm_mode = True
