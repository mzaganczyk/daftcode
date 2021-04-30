import secrets
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Cookie
from fastapi import HTTPException
from fastapi import Response

import hashlib

security = HTTPBasic() # do użycia BasicAuth

app = FastAPI()
app.last_login_session = ""
app.last_login_token = ""

@app.post("/login_session", status_code=201)
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)): # pobiera user i password za pomocą BasicAuth
    #return {"username": credentials.username, "password": credentials.password} # wydobywanie user i password
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not(correct_password and correct_username):
        raise HTTPException(status_code=401)
    session_token = hashlib.sha256(f"{credentials.username} + {credentials.password}".encode()).hexdigest()
    response.set_cookie(key="session_token", value=session_token)
    app.last_login_session = session_token
    return {"OK"}


@app.post("/login_token", status_code=201)
def login_token(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not(correct_password and correct_username):
        raise HTTPException(status_code=401)
    session_token = hashlib.sha256(f"{credentials.username} + {credentials.password}".encode()).hexdigest()
    app.last_login_token = session_token
    return {"token": session_token}