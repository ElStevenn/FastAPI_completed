from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BINARY, Float, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database import Base
from sqlalchemy.orm import configure_mappers
configure_mappers()

class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    username = Column(String, nullable=False, index=True)
    hashed_password = Column(BINARY, nullable=False)
    is_active = Column(Boolean, default=False)

    books = relationship("Books_", back_populates="owner")
    items = relationship("Item", back_populates="owner")

    @property
    def to_dict(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'username': self.username,
            'is_active': self.is_active
        }

class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="items")

class Books_(Base):
    __tablename__ = "books_"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid1)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    book_title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    photo_path = Column(String, default="/photos/default.png")
    price = Column(Float, default=0.0)
    content = Column(Text, nullable=False)

    owner = relationship("Users", back_populates="books")

    @property
    def to_dict(self):
        return {
            'id': str(self.id),  
            'owner_id': str(self.owner_id),  
            'book_title': self.book_title,
            'description': self.description,
            'photo_path': self.photo_path,
            'price': self.price,
            'content': self.content
        }



    