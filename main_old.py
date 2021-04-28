# from typing import Optional
# from fastapi import FastAPI, Response, status, HTTPException
# from pydantic import BaseModel
# import hashlib
# import datetime

from starlette.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

class NewUser(BaseModel):
    name: str
    surname: str

class RegisteredUser(BaseModel):
    id: Optional[int]
    name: str
    surname: str
    register_date: Optional[str]
    vaccination_date: Optional[str]


# app = FastAPI()
# app.users = []


@app.get("/")
def root():
    return {"message": "Hello world!"}

@app.get("/auth")
async def check_login(password: str = '', password_hash: str = ''):
    hash = hashlib.sha512()
    hash.update(password.encode('utf-8'))
    if password == '' or password_hash == '':
        return Response(status_code=HTTP_401_UNAUTHORIZED)
    if hash.hexdigest() == password_hash:
        return Response(status_code=HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
        
@app.post("/register", status_code=201)
async def new_user(user: NewUser):
    app.users.append(RegisteredUser(name=user.name, surname=user.surname))
    app.users[-1].id = app.users.index(app.users[-1]) + 1
    today = datetime.date.today()
    length = sum(c.isalpha() for c in app.users[-1].name) + sum(c.isalpha() for c in app.users[-1].surname)
    app.users[-1].register_date = today.strftime("%Y-%m-%d")
    app.users[-1].vaccination_date = (today + datetime.timedelta(days = length)).strftime("%Y-%m-%d")
    return app.users[-1]

@app.get("/patient/{id}", response_model=RegisteredUser)
async def view_patient(id: int):
    if id < 1:
        return Response(status_code=HTTP_400_BAD_REQUEST)
    try:
        return app.users[id-1]
    except IndexError:
        return Response(status_code=HTTP_404_NOT_FOUND)

@app.get("/method")
def check_method():
    return {"method": "GET"}

@app.post("/method", status_code=201)
def check_method():
    return {"method": "POST"}

@app.put("/method")
def check_method():
    return {"method": "PUT"}

@app.options("/method")
def check_method():
    return {"method": "OPTIONS"}

@app.delete("/method")
def check_method():
    return {"method": "DELETE"}