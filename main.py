from fastapi import Cookie, FastAPI, Response
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from datetime import datetime
from starlette.status import HTTP_401_UNAUTHORIZED
import random

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get("/hello")
def root(request: Request):
    return templates.TemplateResponse("index.html.j2",
    {
        "request": request, "date": datetime.today().strftime("%Y-%m-%d")
    })

@app.post("/login_session")
def login(user: str, password: str, response: Response):
    if user == '4dm1n' and password == 'NotSoSecurePa$$':
        session_token = random.getrandbits(16)
        response.set_cookie(key="session_token", value=session_token)
        return {"message": "siema"}
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)


@app.post("/login_token")
def token(user: str, password: str, response: Response):
    if user == '4dm1n' and password == 'NotSoSecurePa$$':
        session_token = random.getrandbits(16)
        return {"token": session_token}
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
