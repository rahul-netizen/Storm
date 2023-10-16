import re
import traceback

import pandas as pd
from fastapi import UploadFile
from models.database.db_manager import Database, DBManager
from models.file.file_manager import FileManager
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_file_extension(filename: str) -> str:
    file_ext_pattern = r"^(.*)\.(.*)$"
    re_xp = re.compile(file_ext_pattern, flags=re.MULTILINE | re.IGNORECASE)
    results = re.match(re_xp, filename)

    if results:
        filename_without_ext = results.group(1)
        ext = results.group(2)
        return filename_without_ext, ext
    return None, None


async def save_file_to_custom_db(file: UploadFile, **kwargs) -> bool:
    db_manager = kwargs.get("db_manager")
    db_file = kwargs.get("db_file")
    # db_engine = db_manager.get_db_client_by_name()
    db_con_string = db_manager.get_connection_string()
    file_manager = FileManager(file.file, db_file.name, db_file.extension)
    print(file_manager)
    try:
        file_manager.read_file_in_chunks(db_con_string)
        return True
    except ValueError as e:
        raise e


# read file
