from sqlalchemy.orm import Session
from models.file import file_models, file_schema
from datetime import datetime
from utils.helpers import get_file_extension

async def get_file(db: Session, filename: str):
    return db.query(file_models.File.name == filename)

async def get_file_by_id(db: Session, file_id: int):
    return db.query(file_models.File).filter(file_models.File.file_id == file_id)

async def get_files(db: Session, skip: int = 0, limit: int = 100):
    return db.query(file_models.File).offset(skip).limit(limit).all()

async def create_file(db: Session, file: file_schema.File):

    filename_without_ext, ext = await get_file_extension(file.name)
    db_file = file_models.File(
        name = filename_without_ext,
        extension = ext,
        upload_date = datetime.now()
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file