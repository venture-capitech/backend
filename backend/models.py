# models.py

from database import Base
import sqlalchemy
import enum


class EntityType(enum.Enum):
    SuperUser = 0   # Bank
    Business = 1
    Personal = 2


class Account(Base):
    __tablename__ = "accounts"

    # fields
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    entityType = sqlalchemy.Column(sqlalchemy.EntityType, index=True)
    balance = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    # relationships
    user = sqlalchemy.orm.relationship("User", back_populates="accounts")


class User(Base):
    __tablename__ = "users"

    # fields
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    # relationships
    accounts = sqlalchemy.orm.relationship("Account", back_populates="user")


class Transaction(Base):
    __tablename__ = "transactions"

    # fields
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    amount = sqlalchemy.Column(sqlalchemy.Integer)
    from_account_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("accounts.id"))
    to_account_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("accounts.id"))

    # relationships
    from_account = sqlalchemy.orm.relationship("Account", foreign_keys=[from_account_id], back_populates="transactions")
    to_account = sqlalchemy.orm.relationship("Account", foreign_keys=[to_account_id], back_populates="transactions")
