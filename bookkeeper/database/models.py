from bookkeeper.database.utils import is_within_chr_limit
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, ForeignKey


class Base(DeclarativeBase):
    id      = Column(Integer, primary_key = True)


class Book(Base):
    __tablename__ = "books"

    title   = Column(String, nullable  = False)
    edition = Column(Integer, nullable = True)
    status  = Column(Integer, nullable  = False)

    author_id = Column(Integer, ForeignKey("authors.id"), nullable = False)
    held_by   = Column(Integer, ForeignKey("users.id"), nullable = True)

    user   = relationship("User", back_populates = "books")
    author = relationship("Author", back_populates = "books")

    def __init__(self, title: str, author_id: int, status: int, edition: int = None):
        self.author_id = author_id
        self.title = title
        self.status = status
        if edition != None: self.edition = edition

    def __repr__(self):
        return f"{self.title} - {self.author}"
    
    def __json__(self):
        return {
                'id':self.id,
                'title':self.title,
                "author_id": self.author_id,
                "edition": self.edition,
                "status":self.status
                }


class Author(Base):
    __tablename__ = 'authors'

    name    = Column(String, nullable = False)
    surname = Column(String, nullable = True)

    books = relationship("Book", back_populates = "author")

    def __repr__(self):
        return f"{self.name} {self.surname}"
    
    def __json__(self):
        return {
            "id":self.id,
            "name":self.name,
            "surname":self.surname
        }

class User(Base):
    __tablename__ = "users"

    name    = Column(String, nullable = False)
    surname = Column(String, nullable = True)

    books = relationship("Book", back_populates = "user")

    def __repr__(self):
        return f"{self.name} {self.surname}"
    