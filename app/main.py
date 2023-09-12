#!/usr/bin/env python3

from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import crud
from models import *
from schemas import *
from database import SessionLocal, engine, inspector
import sys


db = SessionLocal()
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

class User(BaseModel):
    email: str
    hashed_password: str
    is_active: bool | None = False

class items(BaseModel):
    title: str
    description: str | None = ""
    owner_id: uuid.UUID


@app.get("/")
def main():
    return {"Response":"This is a test!"}


@app.get("/get_user/{user_id}")
def get_user_by_id(user_id: str):

    return {"Result":"None"}

@app.get("/show_tables_name", description="Get all the current tables from the database")
def show_tables():
    table_names = inspector.get_table_names()

    return {"Table_Names":table_names}


@app.get("/get_user/{user_id}", description="Get user data with its id |")
async def get_a_user(user_id: str):
    result = crud.get_user(db=db, user_id=user_id)
    return {"response":result}


@app.get("/get_all_users", description="")
async def get_all_users():
    result = crud.get_users(db=db, limit=999)
    return {"response":result}


@app.get("/get_item/{item_id}", description="Get and item ")
async def get_an_item(item_id: str):
    result = crud.get_item(db=db, item_id=item_id)
    return {"response":result}


@app.post("/post_user", description="Add a new user into to User table")
async def post_user(user: User):
    try:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        return {"response": crud.create_user(db=db, user=user)}
    
    finally:
        db.close()


@app.post("/post_item", description="ds")
async def post_item(item: Item):
    try:
        return {"response":}

    finally:
        pass