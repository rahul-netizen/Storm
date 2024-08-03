
from services.db_manager import DBManager
from fastapi import UploadFile
from services.file_manager import FileManager

# async def get_file_extension(filename: str) -> str:
    
#     file_ext_pattern = r"^(.*)\.(.*)$"
#     re_xp = re.compile(file_ext_pattern, flags= re.MULTILINE | re.IGNORECASE)
#     results = re.match(re_xp, filename)
    
#     if results:
#         filename_without_ext = results.group(1)
#         ext = results.group(2)
#         return filename_without_ext, ext
#     return None,None


async def save_file_to_custom_db(file: UploadFile, **kwargs) -> bool :
    
        db_manager: DBManager = kwargs.get('db_manager')
        db_file = kwargs.get('db_file')
        db_engine = db_manager.get_db_client_by_name()
        db_con_string = db_manager.get_connection_string()
        db_schema = db_manager.get_db_schema()
        
        file_manager = FileManager(file.file, db_file.name,db_file.extension)
        # print(file_manager)
        try:     
            file_manager.read_file_in_chunks(db_engine, schema=db_schema)
            return True
        except ValueError as e:
            raise e 

    