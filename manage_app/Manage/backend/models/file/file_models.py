from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from utils.base_database import Base


class File(Base):
    # TODO: test file extension nullable change with migration
    __tablename__ = "file"
    file_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    extension = Column(String, nullable=True)
    upload_date = Column(DateTime, nullable=False)
