from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine import Engine

from contextlib import contextmanager

from dotenv import load_dotenv, find_dotenv
import os

from utils.logger import logger

_ = load_dotenv(find_dotenv(filename='.env.dev'))

POSTGRES_USER = os.getenv('POSTGRES_USER','NOT_PROVIDED_POSTGRES_USER')
POSTGRES_PW = os.getenv('POSTGRES_PW','NOT_PROVIDED_POSTGRES_PW')
POSTGRES_HOST = os.getenv('POSTGRES_HOST','NOT_PROVIDED_POSTGRES_HOST')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT','NOT_PROVIDED_POSTGRES_PORT'))
POSTGRES_DB = os.getenv('POSTGRES_DB','NOT_PROVIDED_POSTGRES_DB')

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername='postgresql',
    username=POSTGRES_USER,
    password=POSTGRES_PW,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=5,
            max_overflow=10,
            pool_pre_ping=True)
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = Base.metadata


def get_db():
    db = sessionlocal()
    try: 
        yield db
    finally:
        db.close()

@contextmanager
def get_custom_db_contxt_session(engine: Engine):
    """Creates a context with an open SQLAlchemy session."""
    db_session, connection = None, None
    try:
        connection = engine.connect()
        db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine, expire_on_commit=False))
        yield db_session
        db_session.commit()
    except (OperationalError, BaseException) as e:
        logger().critical(f"Unable to perform postgres db operation due to error {e}, rolling back")
        if db_session:
            db_session.rollback()
        raise ValueError(f"Unable to perform postgres db operation due to error {e}, rolling back")
    finally:
        if db_session and connection:
            db_session.close()
            connection.close()
# alembic revision --autogenerate -m "First commit"