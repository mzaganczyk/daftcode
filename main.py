from fastapi import Cookie, FastAPI, Response, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.requests import Request
from datetime import datetime
from starlette.status import HTTP_401_UNAUTHORIZED
import random

app = FastAPI()
app.tokens = []
templates = Jinja2Templates(directory='templates')

security = HTTPBasic()

@app.get("/hello")
def root(request: Request):
    return templates.TemplateResponse("index.html.j2",
    {
        "request": request, "date": datetime.today().strftime("%Y-%m-%d")
    })

@app.post("/login_session")
def login(response: Response, user: str = '', password: str = ''):
    if not (user == '4dm1n' and password == 'NotSoSecurePa$$'):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    else:
        session_token = random.getrandbits(16)
        app.tokens.append(session_token)
        response.set_cookie(key="session_token", value=session_token)
        return {"message": 'OK'}

@app.post("/login_token")
def token(*, response: Response, session_token: str = Cookie(None)):
    return {"token": session_token}