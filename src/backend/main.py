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


from models.file import file_models
from routers import file_routers, user_routers, auth_routers
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

file_models.Base.metadata.create_all(bind=engine)

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
app.include_router(google_auth_routers.router)
app.include_router(basic_auth_routers.router)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# region FusionAuth
# Fusion Auth
# oauth.register(
#     "FusionAuth",
#     client_id=env.get("CLIENT_ID"),
#     client_secret=env.get("CLIENT_SECRET"),
#     client_kwargs={
#         "scope": "openid offline_access",
#         # 'code_challenge_method': 'S256'  # This enables PKCE
#     },
#     server_metadata_url=f'{env.get("ISSUER")}/.well-known/openid-configuration'
# )
# app.fusionauth = FusionAuthClient(
#     api_key=env.get(
#         'FA_API_KEY', "y8Cy_ZG5i6gEMoWT3fmV8N6MVdDrJ8YkHbM1B331RHPaTDjwQmiK7Mv8"),
#     base_url=env.get('ISSUER'))

# def get_logout_url():
#   return 'http://localhost:9011' + "/oauth2/logout?" + urlencode({"client_id": env.get("CLIENT_ID")}, quote_via=quote_plus)


# #region index page
# @app.get("/")
# def home(request: Request):
#     data = {
#         'request': request,
#         'message': 'Hello World !'
#     }
#     user = request.session.get('user')
#     if user is not None:
#         data.update({"user":user}) 
#     print(f"Session : {request.session}")  
#     print(f"User    : {user}") 
#     return templates.TemplateResponse('index.html', context=data, status_code=status.HTTP_200_OK)
    
# #endregion

# @app.get('/logout')
# def logout(request: Request):
#     request.session.clear()
#     return RedirectResponse(env.get('ISSUER') + '/oauth2/logout?client_id=' + env.get('CLIENT_ID'))

# @app.get('/login')
# def login(request: Request):
#     fusionauth = OAuth2Session(env.get('CLIENT_ID'), redirect_uri=env.get("REDIRECT_URL","http://127.0.0.1:8000/oauth-redirect"))
#     authorization_url, state = fusionauth.authorization_url(env.get('AUTHORIZATION_BASE_URL','http://localhost:9011/oauth2/authorize'))
#     # registration lives under non standard url, but otherwise takes exactly the same parameters
#     registration_url = authorization_url.replace("authorize","register", 1)

#     # State is used to prevent CSRF, keep this for later.
#     request.session['oauth_state'] = state

#     return RedirectResponse(registration_url)

# # callback
# @app.get('/oauth-redirect')
# @app.get('/callback')
# def callback(request: Request):
#     expected_state = request.session.get('oauth_state')
#     state = request.query_params.get('state', '')

#     print(f"Expected state : {expected_state} \n Current state: {state}")
#     if state != expected_state:
#         print("Error, state doesn't match, redirecting without getting token.")
#         return RedirectResponse('/')
    
#     fusionauth = OAuth2Session(env.get('CLIENT_ID'), redirect_uri=env.get("REDIRECT_URL","http://127.0.0.1:8000/oauth-redirect"))
#     url = request.url
#     # print("URL STR",str(url))
#     params = dict(parse_qsl(((request.url).query)))
#     print("params code", params['code'])
    
#     token = fusionauth.fetch_token(env.get("TOKEN_URL","http://localhost:9011/oauth2/token"), client_secret=env.get("CLIENT_SECRET"),authorization_response=str(request.url))

#     request.session['token'] = token
#     request.session['user'] = fusionauth.get(env.get("USERINFO_URL","http://localhost:9011/oauth2/userinfo"))
#     return RedirectResponse('/')
# endregion




@app.get('/health')
def health_check(request: Request):
    logger.info("helloooo")
    return HTMLResponse("<p> Hello world</p>", status_code=status.HTTP_200_OK)
    # return RedirectResponse("https://www.google.com/")

from utils.logger import setting_otlp
setting_otlp(app, "Storm" )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000,
                log_level="debug", reload=True,)
    # uvicorn main:app --reload
