from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import uuid

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True,default=str((uuid.uuid4())))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False) # Make this please
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, index=True, default=str((uuid.uuid4())))
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")