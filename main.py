import secrets
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Cookie
from fastapi import HTTPException
from fastapi import Response
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from random import randint
import hashlib

from starlette.responses import RedirectResponse

security = HTTPBasic()

app = FastAPI()
app.login_session = ""
app.login_token = ""
app.login_session_three = []
app.login_token_three = []

@app.post("/login_session", status_code=201)
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not(correct_password and correct_username):
        raise HTTPException(status_code=401)
    session_token = hashlib.sha256(f"{credentials.username}{credentials.password}{randint(1,10000)}".encode()).hexdigest()
    response.set_cookie(key="session_token", value=session_token)
    app.login_session = session_token
    app.login_session_three.append(session_token)
    if len(app.login_session_three) > 3:
        app.login_session_three.pop(0)
    return {}


@app.post("/login_token", status_code=201)
def login_token(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not(correct_password and correct_username):
        raise HTTPException(status_code=401)
    session_token = str(hashlib.sha256(f"{credentials.username}{credentials.password}{randint(1,10000)}".encode()).hexdigest())
    app.login_token = session_token
    app.login_token_three.append(session_token)
    if len(app.login_token_three) > 3:
        app.login_token_three.pop(0)
    return {"token": session_token}


@app.get("/welcome_session", status_code=200)
def welcome_session(session_token: str = Cookie(None), format: str = 'plain'):
    if session_token not in app.login_session_three:
        raise HTTPException(status_code=401)
    else:
        if format == 'plain' or format == '':
            return PlainTextResponse(content='Welcome!')
        elif format == 'json':
            return JSONResponse(content={"message": "Welcome!"})
        elif format == 'html':
            return HTMLResponse(content='<h1>Welcome!</h1>')

@app.get("/welcome_token", status_code=200)
def welcome_token(token: str, format: str = 'plain'):
    if token not in app.login_token_three:
        raise HTTPException(status_code=401)
    else:
        if format == 'plain' or format == '':
            return PlainTextResponse(content='Welcome!')
        elif format == 'json':
            return JSONResponse(content={"message": "Welcome!"})
        elif format == 'html':
            return HTMLResponse(content='<h1>Welcome!</h1>')

@app.delete("/logout_session")
def logout_session(format: str = 'plain', session_token: str = Cookie(None)):
    if session_token not in app.login_session_three:
        raise HTTPException(status_code=401)
    else:
        app.login_session_three.remove(session_token)
        return RedirectResponse(url=f'/logged_out?format={format}', status_code=302)

@app.delete("/logout_token")
def logout_token(token: str, format: str = 'plain'):
    if token not in app.login_token_three:
        raise HTTPException(status_code=401)
    else:
        app.login_token_three.remove(token)
        return RedirectResponse(url=f'/logged_out?format={format}', status_code=302)

@app.get("/logged_out", status_code=200)
def logged_out(format: str = 'plain'):
    if format == 'plain' or format == '':
        return PlainTextResponse(content='Logged out!')
    elif format == 'json':
        return JSONResponse(content={"message": "Logged out!"})
    elif format == 'html':
        return HTMLResponse(content='<h1>Logged out!</h1>')

