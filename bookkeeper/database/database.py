from bookkeeper.database.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import  Session
from sqlalchemy import Column, Integer, String

from bookkeeper.database.DTO import Book, Author, Library, User

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
            if value == None: ValueError("This DB message requires additional field - value")
            self.value = value
        else: self.value = None

    def __repr__(self):
        if self.value != None:
            return self.value.__repr__()
        return self.message.__repr__()
    
    def __str__(self):
        if self.value != None:
            return self.value.__str__()
        return self.message.__str__()
    
    def __json__(self):
        if self.message == DBMessage.OBJECT or self.message == DBMessage.CREATED: return self.value.__json__()
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
            book = book.db()
            session.add(book)
            session.commit()
            return DBResponse(DBMessage.CREATED, book.id)
        else:
            return DBResponse(DBMessage.AUTHOR_NOT_FOUND)

    def add_author(self, author: Author) -> DBResponse:
        session =  Session(bind = self.engine)
        author = author.db()
        session.add(author)
        session.commit()
        return DBResponse(DBMessage.CREATED, author.id)
    
    def add_user(self, user: User) -> DBResponse:
        session =  Session(bind = self.engine)
        user = user.db()
        session.add(user)
        session.commit()
        return DBResponse(DBMessage.CREATED, user.id)

    def add_library(self, library: Library) -> DBResponse:
        session =  Session(bind = self.engine)
        library = library.db()
        session.add(library)
        session.commit()
        return DBResponse(DBMessage.CREATED, library.id)

    def get_books(self) -> DBResponse:
        session =  Session(bind = self.engine)
        resp =  DBResponse(DBMessage.OBJECT_LIST, [Book.from_db(obj) for obj in session.query(BookSchema).all()])
        session.close()
        return resp 
    
    def get_authors(self) -> DBResponse:
        session =  Session(bind = self.engine)
        resp =  DBResponse(DBMessage.OBJECT_LIST, [Author.from_db(obj) for obj in session.query(AuthorSchema).all()])
        session.close()
        return resp 
    
    def get_users(self) -> DBResponse:
        session =  Session(bind = self.engine)
        resp =  DBResponse(DBMessage.OBJECT_LIST, [User.from_db(obj) for obj in session.query(UserSchema).all()])
        session.close()
        return resp 
    
    #for now all the libraries belong only to one user, but just in case
    def get_libraries_by_user(self, user_id) -> DBResponse:
        session =  Session(bind = self.engine)
        resp = DBResponse(DBMessage.OBJECT_LIST, [Library.from_db(obj) for obj in session.query(LibrarySchema).all()])
        session.close()
        return resp 
    
    def get_library_by_id(self, id):
        session = Session(bind = self.engine)
        resp = DBResponse(DBMessage.OBJECT , Library.from_db(session.query(LibrarySchema).where(LibrarySchema.id == id).first()))
        session.close()
        return resp 

    def get_books_by_author_id(self, author_id) -> DBResponse:
        session =  Session(bind = self.engine)
        resp =  DBResponse(DBMessage.OBJECT_LIST, [Book.from_db(obj) for obj in session.query(AuthorSchema).where(AuthorSchema.id == author_id).first().books])
        session.close()
        return resp 
    
    def get_books_by_user_id(self, user_id) -> DBResponse:
        session =  Session(bind = self.engine)
        resp =  DBResponse(DBMessage.OBJECT_LIST, [Book.from_db(obj) for obj in session.query(UserSchema).where(UserSchema.id == user_id).first().books])
        session.close()
        return resp 
    

    def get_book_by_id(self, id: int) -> DBResponse:
        session = Session(bind = self.engine)
        resp =  DBResponse(DBMessage.OBJECT , Book.from_db(session.query(BookSchema).where(BookSchema.id == id).first()))
        session.close()
        return resp 
    
    def get_books_by_library(self, library_id : int) -> DBResponse:
        session =  Session(bind = self.engine)
        resp =  DBResponse(DBMessage.OBJECT_LIST, [Book.from_db(obj) for obj in session.query(LibrarySchema).where(LibrarySchema.id == library_id).first().books])
        session.close()
        return resp 
    
    def get_author_by_id(self, id: int) -> DBResponse:
        session = Session(bind = self.engine)
        resp =  DBResponse(DBMessage.OBJECT, Author.from_db(session.query(AuthorSchema).where(AuthorSchema.id == id).first()))
        session.close()
        return resp 
    
    def get_user_by_id(self, id: int) -> DBResponse:
        session = Session(bind = self.engine)
        resp =  DBResponse(DBMessage.OBJECT, User.from_db(session.query(UserSchema).where(UserSchema.id == id).first()))
        return resp
    
    def does_author_exist(self, author_id) -> bool:
        try:
            return self.get_author_by_id(author_id) != None
        except:
            return False
        
    def delete_book(self, id):
        session = Session(bind = self.engine)
        book = session.query(BookSchema).where(BookSchema.id == id).first()
        if book: 
            session.delete(book)
            session.commit()
            return DBResponse(DBMessage.DELETED, id)
        return DBResponse(DBMessage.BOOK_NOT_FOUND)

    def modify_book(self, id, **options) -> DBResponse:
        session = Session(bind = self.engine)
        book = session.query(BookSchema).where(BookSchema.id == id).first()
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