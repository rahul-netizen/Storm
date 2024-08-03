from fastapi import APIRouter, Depends, status, Form, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from typing import Annotated

from models.file import schema, crud
from models.file.schema import UploadFileRequest, UploadFileResponse, UploadFileError
from sqlalchemy.orm import Session

from utils.base_database import  get_db
from utils.helpers import save_file_to_custom_db

from services.db_manager import DBManager
from utils.logger import logger

router = APIRouter(prefix='/api',tags=['file'])
templates = Jinja2Templates(directory='templates')

@router.get('/files', response_model=list[schema.File], tags=['file'])
async def read_files(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    files = await crud.get_files(skip=skip, limit=limit, db=db)
    return files


@router.post('/upload_file',description='Upload a file to the destination via replace', status_code=status.HTTP_200_OK,
             responses={
               status.HTTP_200_OK : {"model": UploadFileResponse},
               status.HTTP_400_BAD_REQUEST : {"model": UploadFileError},
           })
# async def upload_files_to_db(request: Request):
# You can declare multiple File and Form parameters in a path operation,
# but you can't also declare Body fields that you expect to receive as JSON,
#  as the request will have the body encoded using multipart/form-data instead of application/json.
# This is not a limitation of FastAPI, it's part of the HTTP protocol.
async def upload_files_to_db(files: list[UploadFile], json_file: Annotated[UploadFile, Form(...)] = None, db: Session = Depends(get_db), upload_file_request: UploadFileRequest = Depends()):
    
    # schema name caused "/usr/local/lib/python3.10/site-packages/pydantic/_internal/_fields.py:184: UserWarning: Field name "schema" shadows an attribute in parent "BaseModel"; "
    for file in files:
        # save file details to the central db
        file_model = schema.File(name=file.filename)
        db_file = await crud.create_file(db=db, file=file_model)
        db_manager = DBManager(upload_file_request.username, upload_file_request.password, upload_file_request.hostname, upload_file_request.port, upload_file_request.database_name, upload_file_request.db_schema, upload_file_request.database)

        try:
            upload_status = await save_file_to_custom_db(file=file, db_file=db_file, db_manager=db_manager)
            if not upload_status:
                raise UploadFileError(detail='Could not process the uploaded files!')
            return UploadFileResponse(response=upload_status, files=[file.filename for file in files])
        
        except BaseException as e:
            logger.error(e, exc_info=1)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
