from pydantic import BaseModel
import uuid

class ItemBase(BaseModel):
    title: str | None
    description: str | None
    owner_id: str 

class SingleUser(BaseModel):
    username: str | None
    password: str | None

class BookBase(BaseModel):
    owner_id: str | None = None
    book_name: str
    description: str
    photo_path: str = '/photos/default.png'
    content: str

class CreateBook(BookBase):
    """It's the BookBase but i have to create this"""
    pass

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: uuid.UUID
    owner_id: str

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str | None = None
    username: str | None = None
    is_active: bool | None = False

class UserCreate(UserBase):
    password: str

class UserUpdate(UserCreate):
    pass

class ItemUpdate(ItemBase):
    pass


class User(UserBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
