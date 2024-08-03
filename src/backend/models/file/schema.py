from models.base_schema import BaseModel, ConfigDict
from datetime import datetime
from common.all_enums import DBOptions
from typing import Annotated

class FileBase(BaseModel):
    upload_date: datetime | None = None
    extension: str | None = None
    file_id: int | None = None


class File(FileBase):
    model_config = ConfigDict(from_attributes=True)
    
    name: str




class UploadFileRequest(BaseModel):
    database: DBOptions
    username: str
    hostname: str
    password: str
    database_name: str
    port: int = 5432
    db_schema: str = "public"


class UploadFileResponse(BaseModel):
    response: bool
    files: list

class UploadFileError(BaseModel):
    details: str