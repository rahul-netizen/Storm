from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from utils.base_database import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False ,server_default=func.now())
    updated_at = Column(DateTime, nullable=False ,server_default=func.now())