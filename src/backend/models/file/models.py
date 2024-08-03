from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from utils.base_database import Base

class File(Base):
    # TODO: test file extension nullable change with migration
    __tablename__ = 'files'
    file_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    extension = Column(String, nullable=True)
    upload_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False ,server_default=func.now())
    updated_at = Column(DateTime, nullable=False ,server_default=func.now())