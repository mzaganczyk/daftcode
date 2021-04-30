import secrets
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Cookie
from fastapi import HTTPException
from fastapi import Response
from fastapi.responses import HTMLResponse, JSONResponse

import hashlib

from pydantic.networks import HttpUrl

security = HTTPBasic()

app = FastAPI()
app.login_session = ""
app.login_token = ""

@app.post("/login_session", status_code=201)
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not(correct_password and correct_username):
        raise HTTPException(status_code=401)
    session_token = hashlib.sha256(f"{credentials.username}{credentials.password}".encode()).hexdigest()
    response.set_cookie(key="session_token", value=session_token)
    app.login_session = session_token
    return {}


@app.post("/login_token", status_code=201)
def login_token(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not(correct_password and correct_username):
        raise HTTPException(status_code=401)
    session_token = str(hashlib.sha256(f"{credentials.username}{credentials.password}".encode()).hexdigest())
    app.login_token = session_token
    return {"token": session_token}


@app.get("/welcome_session", status_code=200)
def welcome_session(session_token: str = Cookie(None), format: str = 'plain'):
    if session_token != app.login_session:
        raise HTTPException(status_code=401)
    else:
        if format == 'plain' or format == '':
            return 'Welcome!'
        elif format == 'json':
            return JSONResponse(content={"message": "Welcome!"})
        elif format == 'html':
            return HTMLResponse(content='<h1>Welcome!</h1>')

@app.get("/welcome_token", status_code=200)
def welcome_token(token: str, format: str = 'plain'):
    if token != app.login_token:
        raise HTTPException(status_code=401)
    else:
        if format == 'plain' or format == '':
            return 'Welcome!'
        elif format == 'json':
            return JSONResponse(content={"message": "Welcome!"})
        elif format == 'html':
            return HTMLResponse(content='<h1>Welcome!</h1>')