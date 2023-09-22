from pydantic import BaseModel
import uuid

class ItemBase(BaseModel):
    title: str | None
    description: str | None
    owner_id: str 

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: uuid.UUID
    owner_id: str

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str | None = None
    is_active: bool | None = False

class UserCreate(UserBase):
    hashed_password: str

class UserUpdate(UserCreate):
    pass

class ItemUpdate(ItemBase):
    pass


class User(UserBase):
    id: uuid.UUID

    class Config:
        from_attributes = True