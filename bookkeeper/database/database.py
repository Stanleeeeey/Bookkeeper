from sqlalchemy import create_engine
from sqlalchemy.orm import  Session
from sqlalchemy import Column, Integer, String

from bookkeeper.database.models import Base, Book, Author, User


DB_URL = "sqlite:///example.db"

from enum import Enum

#Possible responses from db
class DBMessage(Enum):
    CREATED = 1
    AUTHOR_NOT_FOUND = 2
    OBJECT_LIST = 3
    OBJECT = 4
    DELETED = 5
    BOOK_NOT_FOUND = 6
    MODIFIED = 7

#Wrapper around DBMessage, that additionally holds value of a reponse, ex. CREATED is supposed to additionally contain id of a created object
class DBResponse:
    def __init__(self, message: DBMessage, value = None):

        self.message = message
        if self.message in [DBMessage.OBJECT, DBMessage.OBJECT_LIST, DBMessage.CREATED, DBMessage.DELETED]:
            if value == None: ValueError("This DB message requires additional field - vlaue")
            self.value = value
        else: self.value = None

    def __repr__(self):
        if self.value != None:
            return self.value
        return self.message
    
    def __json__(self):
        if self.message == DBMessage.OBJECT: return self.value.__json__()
        elif self.message == DBMessage.OBJECT_LIST: return [obj.__json__() for obj in self.value]

    def __iter__(self):
        if self.message == DBMessage.OBJECT_LIST:
            return self.value.__iter__()
        else: ValueError("this response is not iterable")

class Database():
    def __init__(self):
        self.engine = create_engine(DB_URL, echo=False)
        Base.metadata.create_all(self.engine)

    def add_book(self, book: Book) -> DBResponse:
        if self.does_author_exist(book.author_id):
            session =  Session(bind = self.engine)
            session.add(book)
            session.commit()
            return DBResponse(DBMessage.CREATED, book.id)
        else:
            return DBResponse(DBMessage.AUTHOR_NOT_FOUND)

    def add_author(self, author: Author) -> DBResponse:
        session =  Session(bind = self.engine)
        session.add(author)
        session.commit()
        return DBResponse(DBMessage.CREATED, author.id)

    def get_books(self) -> DBResponse:
        session =  Session(bind = self.engine)
        return DBResponse(DBMessage.OBJECT_LIST, session.query(Book).all())
    
    def get_authors(self) -> DBResponse:
        session =  Session(bind = self.engine)
        return DBResponse(DBMessage.OBJECT_LIST, session.query(Author).all())
    
    def get_books_by_author_id(self, author_id) -> DBResponse:
        session =  Session(bind = self.engine)
        return DBResponse(DBMessage.OBJECT_LIST, session.query(Author).where(Author.id == author_id).first().books)
    
    def get_book_by_id(self, id: int) -> DBResponse:
        session = Session(bind = self.engine)
        return DBResponse(DBMessage.OBJECT ,session.query(Book).where(Book.id == id).first())
    
    def get_author_by_id(self, id: int) -> DBResponse:
        session = Session(bind = self.engine)
        return DBResponse(DBMessage.OBJECT, session.query(Author).where(Author.id == id).first())
    
    def does_author_exist(self, author_id) -> bool:
        return self.get_author_by_id(author_id) != None
    
    def delete_book(self, id):
        session = Session(bind = self.engine)
        book = session.query(Book).where(Book.id == id).first()
        if book: 
            session.delete(book)
            session.commit()
            return DBResponse(DBMessage.DELETED, id)
        return DBResponse(DBMessage.BOOK_NOT_FOUND)

    def modify_book(self, id, **options) -> DBResponse:
        session = Session(bind = self.engine)
        book = session.query(Book).where(Book.id == id).first()
        if book:
            if "title" in options:
                book.title = options["title"]
            if "author_id" in options:
                book.author_id = options["author_id"]
            if "edition" in options:
                book.edition = options["edition"]
            if "status" in options:
                book.status = options["status"]

            session.commit()

            return DBResponse(DBMessage.MODIFIED)
        return DBResponse(DBMessage.BOOK_NOT_FOUND)