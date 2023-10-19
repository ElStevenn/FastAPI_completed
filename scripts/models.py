from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BINARY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    username = Column(String, nullable=False,  index=True)
    hashed_password = Column(BINARY, nullable=False)
    is_active = Column(Boolean, default=False)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

class Books(Base):
    __tablename__ = "Books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid1)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    book_name = Column(String, nullable=False)
    description = Column(String(1000), nullable=False)
    photo_path = Column(String, default="/photos/default.png")
    content = Column(String, nullable=False)




    