#!/usr/bin/env python3
from sqlalchemy.orm import Session
from sqlalchemy import select
#from . import models, schemas
from . import models
from . import schemas
from . import encrypt

def get_user(db: Session, user_id: str):
    return db.query(models.Users).filter(models.Users.id == user_id).first()

def get_item(db: Session, item_id: str):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_book(db: Session, book_id: str):
    return db.query(models.Books_).filter(models.Books_.id == book_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()

def get_books(db: Session, skip: int = 0, limit: int = 9999):
    return db.query(models.Books_).offset(skip).limit(limit).all()

def get_books_by_author(db: Session, owner_id: str):
    return (
        db.query(models.Books_.id, models.Books_.book_title, models.Books_.description, models.Books_.photo_path, models.Books_.price, models.Books_.price)
        .join(models.Users, models.Books_.owner_id == models.Users.id)
        .filter(models.Books_.owner_id == owner_id)
        .all()
    )

def get_books_by_id(db: Session, book_id: str):
    return db.query(models.Books_).filter(models.Books_.id == book_id).all()

def fetch_user_password(db: Session, username: str):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        raise ValueError(f"{username} doesn't exists in the users table!")

    return user.hashed_password

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_book(db: Session, book: schemas.CreateBook, owner_id: str):
    db_book = models.Books_(**book.model_dump(), owner_id=owner_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def create_user(db: Session, user: schemas.UserCreate):
    key = encrypt.EncryptPassword.read_key()
    encrypter = encrypt.EncryptPassword(key)

    db_user = models.Users(email=user.email, hashed_password=encrypter.encrypt_passowrd(user.password), username=user.username, is_active=user.is_active)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: schemas.UserCreate, user_id: str):
    try:
        db_user = db.query(models.Users).filter(models.Users.id == user_id).first()
        
        if not db_user:
            return f"User with ID {user_id} not found."

        # Update only the attributes that exist in the db_user model
        for key, value in user.dict().items():
            if hasattr(db_user, key) and value is not None:
                setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return db_user

    except Exception as e:
        return f"An error occurred: {e}"

def update_item(db: Session, item_id: str, item: schemas.ItemUpdate):
    try:
        db_item = db.query(models.Item).filter(models.Item.id == item_id).first()

        if not db_item:
            return f"Item with ID {item_id} not found."

        # Update only the attributes that exist in the db_item model
        for key, value in item.dict().items():
            if hasattr(db_item, key) and value is not None:
                setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)
   
        return db_item
    
    except Exception as e:
        return f"An error ocurred: {e}"

def delete_user(db: Session, user_id: str):
    try:
        user_to_delete = get_user(db=db, user_id=user_id)
        deleted_user = db.delete(user_to_delete)

        db.commit()
        return f"User {deleted_user.email} deleted successfully."
    
    except Exception as e:
        return f"An error ocurred: {e}"
 
def delete_item(db: Session, item_id: str):
    try:
        item_to_delete = get_item(db=db, item_id=item_id)
        db.delete(item_to_delete)

        db.commit()
        return f"Item {item_id} deleted successfully."
    except Exception as e:
        return f"An error ocurred: {e}"

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item