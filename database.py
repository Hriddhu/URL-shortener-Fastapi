from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL= os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing from environment variables!")

engine= create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal= sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass