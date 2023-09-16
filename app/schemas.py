from pydantic import BaseModel
import uuid

class ItemBase(BaseModel):
    title: str
    description: str | None
    owner_id: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: uuid.UUID
    owner_id: str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str | None = None
    is_active: bool | None = False

class UserCreate(UserBase):
    hashed_password: str

class UserUpdate(UserCreate):
    """Solve this issue in the future"""
    pass

class User(UserBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
