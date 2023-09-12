#!/usr/bin/env python3

from fastapi import FastAPI, Path
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from crud import *
from models import *
from schemas import *
from database import SessionLocal, engine
import sys

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You might want to specify exact origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def main():
    return {"Response":"This is a test!"}


@app.get("/get_user/{user_id}")
def get_user_by_id(user_id: str):

    return {"Result":"None"}

@app.get("/show_tables")
def show_tables():

    
    return {}

@app.post("/post_user")
def post_user():
    pass
