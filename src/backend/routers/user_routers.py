from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from models.user import  schemas
from utils.base_database import  get_db

from typing import Annotated, List
from models.user import crud
from utils.authentication import get_current_active_user


router = APIRouter(prefix='/api', tags=['user'])
templates = Jinja2Templates(directory='templates')



class UserSignup():
    def __init__(
        self,
        username: str = Form(),
        password: str = Form(),
        email: str = Form(),
    ):
        self.username = username
        self.password = password
        self.email = email

@router.get("/user/{username}", response_model=schemas.User)
async def read_user(username: str , db: Session = Depends(get_db)):
    user = crud.get_user_by_username(username=username, db=db)
    return user


@router.get('/users',response_model=List[schemas.User], description="Get all users")
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users =  crud.get_users(skip=skip, limit=limit, db=db)
    return users

@router.post('/signup',response_model=schemas.User)
async def create_user(user_form_data: Annotated[UserSignup, Depends()],db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=user_form_data.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists.")
    user = schemas.UserCreate(username=user_form_data.username,hashed_password=user_form_data.password,email=user_form_data.email)
    user = crud.create_user(db=db,user=user)
    return user

@router.get("/users/me")
async def read_user_me(current_user: Annotated[schemas.User, Depends(get_current_active_user)]):
    return current_user