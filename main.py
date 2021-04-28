from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html.j2",
    {
        "request": request, "date": datetime.today().strftime("%Y-%m-%d")
    })