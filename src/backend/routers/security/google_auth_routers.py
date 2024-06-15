from fastapi import APIRouter, Depends, FastAPI, Request, UploadFile, File, Form, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


from authlib.integrations.starlette_client import OAuth
from requests_oauthlib import OAuth2Session
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from os import environ as env
from urllib.parse import quote_plus, urlencode, parse_qsl, urlparse
from dotenv import load_dotenv, find_dotenv
from os import environ


oauth = OAuth()

# print(env.get("GOOGLE_CLIENT_ID"))
# print(env.get("GOOGLE_CLIENT_SECRET"))
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


router = APIRouter()
templates = Jinja2Templates(directory='templates')

# oauth login
@router.get('/login')
async def login(request: Request):
    # absolute url for callback
    # we will define it below
    redirect_uri = request.url_for('auth')
    # return await oauth.FusionAuth.authorize_redirect(request, redirect_uri)
    print(redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)

# oauth redirect or callback
@router.get('/oauth-redirect')
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    print(request.session.items())
    print(f'Tokens : {token["access_token"]}')
    # token = await oauth.FusionAuth.authorize_access_token(request)
    user = token['userinfo']
    request.session.update({"user":dict(user)})
    # return user
    return RedirectResponse('/')

def get_logout_url():
    return 'http://localhost:9011' + "/oauth2/logout?" + urlencode({"client_id": env.get("CLIENT_ID")},quote_via=quote_plus)

@router.get('/logout')
def logout(request: Request):
    request.session.pop('user')
    # return RedirectResponse(get_logout_url())
    return RedirectResponse('/')

@router.get('/', response_class=HTMLResponse)
def home(request: Request) :
    data = {
        'request': request,
        'message': 'Hello World !'
    }
    user = request.session.get('user')
    if user:
        data.update(user)
        # return templates.TemplateResponse('home.html', context=data, status_code=status.HTTP_200_OK)
        html = (
            f'<p>{data}</p>'
            '<a href="https://www.google.com">Google</a></br>'
            '<a href="/logout" method="GET">logout</a></br>'
            '<a href="http://localhost:8501" method="GET">Frontend</a>'
        )
        return HTMLResponse(html)
        # return templates.TemplateResponse('home.html', context=data, status_code=status.HTTP_200_OK)
    return templates.TemplateResponse('login.html', context=data, status_code=status.HTTP_200_OK)
    #     frontend_url = environ.get("FRONTEND_HOST",) + ':' + environ.get("FRONTEND_PORT")
    #     return RedirectResponse(frontend_url)