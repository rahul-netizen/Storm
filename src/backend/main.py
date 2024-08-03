from fusionauth.fusionauth_client import FusionAuthClient
from fastapi import Depends, FastAPI, Request, UploadFile, File, Form, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from sqlalchemy.orm import Session
from utils.base_database import sessionlocal
from utils.logger import logger


from models.file import models
from routers import file_routers, user_routers, auth_routers, health
from routers.security import google_auth_routers, basic_auth_routers
from utils.authentication import get_current_active_user
from utils.base_database import engine
from typing import Annotated
from enum import Enum
import json

from authlib.integrations.starlette_client import OAuth
from requests_oauthlib import OAuth2Session
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from os import environ as env
from urllib.parse import quote_plus, urlencode, parse_qsl, urlparse
from dotenv import load_dotenv, find_dotenv
from os import environ

_ = load_dotenv(find_dotenv())

# config = Config('.env.dev')  # read config from .env file
oauth = OAuth()

# Google SSO
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    },
    client_id=env.get("GOOGLE_CLIENT_ID"),
    client_secret=env.get("GOOGLE_CLIENT_SECRET"),
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
# required for google sso oauth2
app.add_middleware(SessionMiddleware, secret_key=env.get("GOOGLE_SECRET_KEY"))
templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")

# app.include_router(file_routers.router, dependencies=[Depends(get_current_active_user)])
app.include_router(file_routers.router)
# auth urls followed get_current_active_user dependency
app.include_router(auth_routers.router)
# app.include_router(user_routers.router, dependencies=[Depends(get_current_active_user)] ) # authentication dependency
app.include_router(user_routers.router)
# app.include_router(google_auth_routers.router)
app.include_router(basic_auth_routers.router)
app.include_router(health.router)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000,
                log_level="debug", reload=True,)
