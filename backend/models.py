from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class EntityType(enum.Enum):
    SuperUser = 0
    Business = 1
    Personal = 2

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    entityType = Column(Enum(EntityType), index=True)
    balance = Column(Integer, default=0)
    owner = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="from_account", foreign_keys="[Transaction.from_account_id]")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    accounts = relationship("Account", back_populates="user")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    from_account_id = Column(Integer, ForeignKey("accounts.id"))
    to_account_id = Column(Integer, ForeignKey("accounts.id"))

    from_account = relationship("Account", back_populates="transactions", foreign_keys=[from_account_id])
    to_account = relationship("Account", back_populates="transactions", foreign_keys=[to_account_id])
