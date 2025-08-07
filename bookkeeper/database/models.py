from bookkeeper.database.utils import is_within_chr_limit
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, ForeignKey


#MODELS for the database

class Base(DeclarativeBase):
    id      = Column(Integer, primary_key = True)


class BookSchema(Base):
    __tablename__ = "books"

    title   = Column(String, nullable  = False)
    edition = Column(Integer, nullable = True)
    status  = Column(Integer, nullable  = False)

    author_id  = Column(Integer, ForeignKey("authors.id"), nullable = False)
    held_by    = Column(Integer, ForeignKey("users.id"), nullable = True)
    library_id = Column(Integer, ForeignKey("libraries.id"), nullable = False)

    user    = relationship("UserSchema", back_populates = "books")
    author  = relationship("AuthorSchema", back_populates = "books")
    library = relationship("LibrarySchema", back_populates = "books")

    def __init__(self, title: str, author_id: int, status: int, library_id:int,  edition: int = None,held_by : int = None):
        self.author_id = author_id
        self.title = title
        self.status = status
        self.library_id = library_id
        if edition != None: self.edition = edition
        if held_by != None: self.held_by = held_by


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


class LibrarySchema(Base):
    __tablename__ = "libraries"

    name = Column(String, nullable = False)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)

    user   = relationship("UserSchema", back_populates = "libraries")
    books  = relationship("BookSchema", back_populates = "library")

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id



class AuthorSchema(Base):
    __tablename__ = 'authors'

    name    = Column(String, nullable = False)
    surname = Column(String, nullable = True)

    books = relationship("BookSchema", back_populates = "author")

    def __repr__(self):
        return f"{self.name} {self.surname}"
    
    def __json__(self):
        return {
            "id":self.id,
            "name":self.name,
            "surname":self.surname
        }
    
    def __init__(self, name, surname):
        self.name = name
        self.surname=  surname
    

class UserSchema(Base):
    __tablename__ = "users"

    name    = Column(String, nullable = False)
    surname = Column(String, nullable = True)

    books = relationship("BookSchema", back_populates = "user")
    libraries = relationship("LibrarySchema", back_populates = "user")

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def __repr__(self):
        return f"{self.name} {self.surname}"
    
    def __str__(self):
        return f"{self.name} {self.surname}"

    