from fastapi import APIRouter, Response, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from utils.base_database import  get_db

from typing import Annotated
from datetime import timedelta
from utils.authentication import ACCESS_TOKEN_EXPIRE_MINUTES,REFRESH_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token,create_refresh_token, Token

router = APIRouter(prefix='/api', tags=["auth"])

@router.post("/token",summary="Create access and refresh tokens for user", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username} , expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": form_data.username} , expires_delta=refresh_token_expires)
    
    return {"access_token": access_token,"refresh_token":refresh_token, "token_type": "bearer"}