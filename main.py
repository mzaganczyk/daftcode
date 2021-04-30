from fastapi import Cookie, FastAPI, Response, HTTPException, responses
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.requests import Request
from datetime import datetime
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
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
        try:
            app.tokens.pop()
        except IndexError:
            pass
        session_token = str(random.getrandbits(16))
        app.tokens.append(session_token)
        response.set_cookie(key="session_token", value=session_token)
        response.status_code = HTTP_201_CREATED
        return {"tokens": app.tokens}

@app.post("/login_token")
def token(*, response: Response, session_token: str = Cookie(None)):
    if session_token not in app.tokens:
        raise HTTPException(status_code=401)
    else:
        return {"token": session_token}