#!/usr/bin/env python3

from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from typing import Optional
import crud, models, encrypt
from models import *
import schemas 
from database import SessionLocal, engine, inspector
import sys
import uvicorn


db = SessionLocal()
app = FastAPI(
    debug=True,
    title="Login and Register API",
    summary = "This is a login/register application created by Pau Mateu ",
    docs_url= "/documentation",
    description="This will be the long description...",
    version="0.12.2"
)


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
"""
class User(BaseModel):
    email: str
    hashed_password: str
    is_active: bool | None = False
"""
class items(BaseModel):
    title: str
    description: str | None = ""
    owner_id: uuid.UUID


@app.get("/")
def main():
    return {"Response":"Server is actually working, you can use the diferents methods!"}


@app.get("/get_user/{user_id}")
def get_user_by_id(user_id: str):
    try:
        return {"Result": crud.get_user(db=db, user_id=user_id)}
    except:
        return {"Error": f"User {user_id} doesn't exist."}
    finally:
        db.close()


@app.get("/show_tables_name", description="Get all the current tables from the database")
def show_tables():
    table_names = inspector.get_table_names()

    return {"Table_Names":table_names}


@app.get("/get_user/{user_id}", description="Get user data with its id |")
async def get_a_user(user_id: str):
    result = crud.get_user(db=db, user_id=user_id)
    return {"response":result}


@app.get("/get_all_users", description="Get all the users from users table")
async def get_all_users():
    result = crud.get_users(db=db, limit=999)
    return {"response":result}


@app.get("/get_item/{item_id}", description="Get and item from item table")
async def get_an_item(item_id: str):
    result = crud.get_item(db=db, item_id=item_id)
    return {"response":result}


@app.post("/post_user", description="Add a new user into to User table")
async def post_user(user: schemas.UserCreate):
    # In this function there are an error when we create another consecutive user, solve it.
    try:
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        return {"response": crud.create_user(db=db, user=user)}

    except Exception.IntegrityError:
        raise HTTPException(status_code=400, detail="Duplicate item ID or other integrity error")   

    finally:
        db.close()


@app.post("/post_item", description="Post new item into item table")
async def post_item(item: schemas.ItemCreate):
    try:
        user = crud.get_user(db, str(item.owner_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"response": crud.create_item(db=db, item=item, )}
    finally:
        db.close()


@app.put("/update_user/{user_id}", description="Update an user from the users table")
async def update_user(user_id: str, user: schemas.UserUpdate):
    try:
        if not user_id:
            raise HTTPException(status_code=404, detail="Invalid input (PUT /update_user/<user_id>)")
        
        return {"Response": crud.update_user(db=db, user_id=user_id, user=user)}

    finally:
        db.close()


@app.put("/update_item/{item_id}", description="Updatea single item from items table")
async def update_item(item_id: str, item: schemas.ItemUpdate):
    try:
        if not item_id:
            raise HTTPException(status_code=404, detail="Invalid input (PUT /update_item/<item_id>)")
        
        return {"Response": crud.update_item(db=db, item_id=item_id, item=item)}

    finally:
        db.close()


@app.delete("/delete_user/{user_id}", description="Delete an user from the user table")
async def delete_user(user_id: str):
    # Change note deleted
    try:
        if not user_id:
            raise HTTPException(status_code=404, detail="Invalid input (DELETE /delete_user<user_id>)")

        return {"Response": crud.delete_user(db=db, user_id=user_id)}
    
    finally:
        db.close()

@app.delete("/delete_item/{item_id}", description="Delete an item from the item table")
async def delet_item(item_id: str):
    try:
        if not item_id:
            raise HTTPException(status_code=404, detail="Invalid input (DELETE /delete_item/<item_id>)")

        
        return {"Response": crud.delete_item(db=db, item_id=item_id)}
    
    finally:
        db.close()

@app.post("/check_user", description="Check if user exists in the user table")
async def check_if_user(User: schemas.SingleUser):
    try:
        if not User.username or not User.hashed_password:
            raise HTTPException(status_code=404, detail="Invalid input (GET /check_user/<user_name>/<hashed_password>)")

        # Decrypt password
        key = encrypt.EncryptPassword.read_key()
        cipher = encrypt.EncryptPassword(key)

        Decrypt_Password = cipher.decrypt_password()

        # Change this when I will implement the hashed passwords
        user = db.query(models.User).filter(
        models.User.username == User.username,
        models.User.hashed_password == User.hashed_password
        ).first()

        if user:
            return {"result": True}
        return {"result": False}
    

    finally:
        
        db.close()
    
@app.get("/get_password/{username}", description="Get hashed password by its username from user table")
async def get_user_password(username: str):
    try:
        if not username:
            raise HTTPException(status_code=404, detail="Invalid input (GET /get_password/<username>)")

        crypted_password = crud.fetch_user_password(db=db, username=username)

        Key = encrypt.EncryptPassword.read_key()
        Encrypter = encrypt.EncryptPassword(Key)

        decrypted_password = Encrypter.decrypt_password(crypted_password)
        
        return {"password": decrypted_password}
    

    finally:
        db.close()
        


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port = 8432,
        reload=True
    )