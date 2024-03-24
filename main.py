from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/login")
def login_method():
    return {"login": "ok"}


@app.get("/signup")
def login_method():
    return {"login": "ok"}

/* Rectangle 15 */

position: absolute;
width: 430px;
height: 932px;
left: 0px;
top: 0px;


