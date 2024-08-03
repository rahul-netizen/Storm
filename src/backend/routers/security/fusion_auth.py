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
