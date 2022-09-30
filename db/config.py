import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

DATBASE_USER = os.getenv("PG_USER")
DATABASE_PASSWORD = os.getenv("PG_PASSWORD")
DATABASE_HOST = os.getenv("PG_HOST")
DATABASE_PORT = os.getenv("PG_PORT")
DATABASE_NAME = os.getenv("PG_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DATBASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
