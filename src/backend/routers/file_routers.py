from fastapi import APIRouter, Depends, HTTPException, status, Request, Form, status, File, UploadFile
from fastapi.templating import Jinja2Templates
from typing import Annotated

from models.file import crud, file_schema, file_models
from sqlalchemy.orm import Session

from utils.base_database import sessionlocal
from utils.helpers import save_file_to_custom_db

from models.database.db_manager import Database, DBManager
from common.all_enums import DBOptions

from pydantic import BaseModel
import json

router = APIRouter()
templates = Jinja2Templates(directory='templates')


async def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/files', response_model=list[file_schema.File], tags=['file'])
async def read_files(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    files = await crud.get_files(skip=skip, limit=limit, db=db)
    return files


@router.post('/file', response_model=file_schema.File)
async def create_file(file: file_schema.File, db: Session = Depends(get_db)):
    # debug this , how to pass id as primarykey
    # db_file = crud.get_file_by_id(db=db, file_id=file.id)
    # if db_file:
    # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='File already exists!')
    return await crud.create_file(db=db, file=file)


@router.get('/upload_file')
async def upload_file_form(request: Request):
    data = {
        'request': request,
        'db_options': DBOptions
    }
    return templates.TemplateResponse('db_file_upload.html', context=data, status_code=status.HTTP_200_OK)

@router.post('/upload_file', status_code=status.HTTP_200_OK)
# async def upload_files_to_db(request: Request):
# You can declare multiple File and Form parameters in a path operation,
# but you can't also declare Body fields that you expect to receive as JSON,
#  as the request will have the body encoded using multipart/form-data instead of application/json.
# This is not a limitation of FastAPI, it's part of the HTTP protocol.
async def upload_files_to_db(database: Annotated[str, Form()],
                             username: Annotated[str, Form()],
                             hostname: Annotated[str, Form()],
                             password: Annotated[str, Form()],
                             database_name: Annotated[str, Form(...)],
                             files: Annotated[list[UploadFile], Form(...)],
                             json_file: Annotated[UploadFile, Form(...)] = None,
                             db: Session = Depends(get_db),
                             port: Annotated[int, Form()] = 5432,
                             db_schema: Annotated[str, Form(...)] = "public"):
    
    # schema name caused "/usr/local/lib/python3.10/site-packages/pydantic/_internal/_fields.py:184: UserWarning: Field name "schema" shadows an attribute in parent "BaseModel"; "
    for file in files:
        # save file details to the central db
        file_model = file_schema.File(name=file.filename)
        db_file = await crud.create_file(db=db, file=file_model)

        db_mananger = DBManager(
            username, password, hostname, port, database_name, db_schema, database)
        try:
            # print(json_file.file.read())
            # print(f"json file {json.loads(json_file.file.read())}")
            upload_status = await save_file_to_custom_db(file=file, db_file=db_file, db_manager=db_mananger)
            if not upload_status:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Could not process the uploaded files!')
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # return templates.TemplateResponse('db_file_upload.html',context= data, status_code=status.HTTP_200_OK)
