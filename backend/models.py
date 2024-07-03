from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy import Enum as sql_enum

from sqlalchemy.orm import relationship
from .database import Base

from enum import auto, Enum


class EntityType(Enum):
    SuperUser = auto()
    Business = auto()
    Personal = auto()


class Account(Base):
    __tablename__ = "accounts"

    # todo change ID to use uuid/ hex/ long long int instead. i rather it not be via auto increament -@scott
    id = Column(Integer, primary_key=True, index=True)
    entityType = Column(sql_enum(EntityType), index=True)
    balance = Column(Integer, default=0)
    owner = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="from_account", foreign_keys="[Transaction.from_account_id]")


class User(Base):
    __tablename__ = "users"

    # todo change ID to use uuid/ hex/ long long int instead. i rather it not be via auto increament -@scott
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    accounts = relationship("Account", back_populates="user")


class Transaction(Base):
    __tablename__ = "transactions"

    # todo change ID to use uuid/ hex/ long long int instead. i rather it not be via auto increament -@scott
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    from_account_id = Column(Integer, ForeignKey("accounts.id"))
    to_account_id = Column(Integer, ForeignKey("accounts.id"))

    from_account = relationship("Account", back_populates="transactions", foreign_keys=[from_account_id])
    to_account = relationship("Account", back_populates="transactions", foreign_keys=[to_account_id])
