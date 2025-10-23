from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from typing import Generator
import os

load_dotenv() # load environment variable


DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL) #Create database engine

#Create the session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


#Create the Base class
class Base(DeclarativeBase):
    pass


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db   # give the session to the request
    finally:
        db.close() # close it after request ends