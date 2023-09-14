from pydantic import BaseModel
import uuid

class ItemBase(BaseModel):
    title: str
    description: str | None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: uuid.UUID
    owner_id: str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: uuid.UUID
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
