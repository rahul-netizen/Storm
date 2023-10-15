from datetime import datetime, timedelta
from typing import Annotated, List, Optional

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from models.user import crud, user_models, user_schemas
from sqlalchemy.orm import Session
from utils.authentication import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_current_user,
)
from utils.base_database import sessionlocal

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


class UserSignup:
    def __init__(
        self,
        username: str = Form(),
        password: str = Form(),
        email: str = Form(),
    ):
        self.username = username
        self.password = password
        self.email = email


@router.get("/user/{username}", response_model=user_schemas.User)
async def read_user(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(username == username, db=db)
    return user


@router.get(
    "/users",
    response_model=List[user_schemas.User],
    description="Get all users",
)
async def read_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    users = crud.get_users(skip=skip, limit=limit, db=db)
    return users


@router.post("/signup", response_model=user_schemas.User)
async def create_user(
    user_form_data: Annotated[UserSignup, Depends()],
    db: Session = Depends(get_db),
):
    db_user = crud.get_user_by_username(db=db, username=user_form_data.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists.",
        )
    user = user_schemas.UserCreate(
        username=user_form_data.username,
        hashed_password=user_form_data.password,
        email=user_form_data.email,
    )
    user = crud.create_user(db=db, user=user)
    return user


@router.get("/users/me")
async def read_user_me(
    current_user: Annotated[user_schemas.User, Depends(get_current_active_user)]
):
    return current_user
