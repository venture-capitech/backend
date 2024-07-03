# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# engine instance, all SQL statements made by program when interacting w DB will be logged to the console.
# engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# my fiddling
# Create DB tables (uncomment if needed)
# Base.metadata.create_all(bind=engine)

# Dependency for getting a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example function to add a user
def add_user(name: str, email: str):
    db = SessionLocal()
    new_user = User(name=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user

# Example function to get all users
def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

# Example function to get a user by ID
def get_user_by_id(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    return user