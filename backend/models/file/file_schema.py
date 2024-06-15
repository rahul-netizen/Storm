from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class FileBase(BaseModel):
    upload_date: datetime | None = None
    extension: str | None = None
    file_id: int | None = None

class FileCreate(FileBase):
    pass
    # class Config:
    #     orm_mode = True

class File(FileBase):
    name: str
    
    # class Config:
    #      orm_mode = True




