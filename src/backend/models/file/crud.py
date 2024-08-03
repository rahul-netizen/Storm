from sqlalchemy.orm import Session
from models.file import models, schema
from datetime import datetime

from pathlib import Path

async def get_file(db: Session, filename: str):
    return db.query(models.File.name == filename)

async def get_file_by_id(db: Session, file_id: int):
    return db.query(models.File).filter(models.File.file_id == file_id)

async def get_files(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.File).offset(skip).limit(limit).all()

async def create_file(db: Session, file: schema.File):

    filename_without_ext, ext =  Path(file.name).stem, Path(file.name).suffix
    db_file = models.File(
        name = filename_without_ext,
        extension = ext,
        upload_date = datetime.now()
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file