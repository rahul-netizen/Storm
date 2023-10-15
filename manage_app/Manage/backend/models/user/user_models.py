from sqlalchemy import (
    BOOLEAN,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from utils.base_database import Base


class User(Base):
    __tablename__ = "User"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
