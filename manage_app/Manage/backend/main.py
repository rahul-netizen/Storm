import json
from enum import Enum
from os import environ as env
from typing import Annotated
from urllib.parse import quote_plus, urlencode

from authlib.integrations.starlette_client import OAuth
from fastapi import (
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models.file import file_models
from pydantic import BaseModel
from routers import auth_routers, file_routers, user_routers
from sqlalchemy.orm import Session
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from utils.authentication import get_current_active_user
from utils.base_database import engine, sessionlocal

config = Config(".env")  # read config from .env file

oauth = OAuth(config)

# Google SSO
oauth.register(
    name="google",
    server_metadata_url=(
        "https://accounts.google.com/.well-known/openid-configuration"
    ),
    client_kwargs={"scope": "openid email profile"},
)

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


file_models.Base.metadata.create_all(bind=engine)


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret-string")


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(
    file_routers.router, dependencies=[Depends(get_current_active_user)]
)

# auth urls followed get_current_active_user dependency
app.include_router(auth_routers.router)

# app.include_router(user_routers.router, dependencies=[Depends(get_current_active_user)] ) # authentication dependency
app.include_router(user_routers.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# oauth login
@app.get("/login")
async def login(request: Request):
    # absolute url for callback
    # we will define it below
    redirect_uri = request.url_for("auth")
    # return await oauth.FusionAuth.authorize_redirect(request, redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)


# oauth redirect or callback
# @app.route('/auth')
@app.get("/oauth-redirect")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    print(request.session.items())
    # token = await oauth.FusionAuth.authorize_access_token(request)
    user = token["userinfo"]
    request.session.update({"user": dict(user)})
    # return user
    return RedirectResponse(request.url_for("home"))


def get_logout_url():
    return (
        "http://localhost:9011"
        + "/oauth2/logout?"
        + urlencode({"client_id": env.get("CLIENT_ID")}, quote_via=quote_plus)
    )


@app.get("/logout")
def logout(request: Request):
    request.session.pop("user")
    return RedirectResponse(get_logout_url())


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    data = {"request": request, "message": "Hello World !"}
    user = request.session.get("user")
    if user:
        return templates.TemplateResponse(
            "home.html", context=data, status_code=status.HTTP_200_OK
        )
        data = json.dumps(user)
        html = f'<pre>{data}</pre><a href="/logout">logout</a>'
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        log_level="debug",
        reload=True,
    )
    # uvicorn main:app --reload
