import os

from dotenv import find_dotenv, load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

_ = load_dotenv(find_dotenv())

POSTGRES_USER = os.getenv("POSTGRES_USER", "NOT_PROVIDED_POSTGRES_USER")
POSTGRES_PW = os.getenv("POSTGRES_PW", "NOT_PROVIDED_POSTGRES_PW")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "NOT_PROVIDED_POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "NOT_PROVIDED_POSTGRES_PORT"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "NOT_PROVIDED_POSTGRES_DB")

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql",
    username=POSTGRES_USER,
    password=POSTGRES_PW,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB,
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = Base.metadata

# alembic revision --autogenerate -m "First commit"
