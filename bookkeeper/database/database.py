"""Read, edit, add to database"""
import sys
import os
from enum import Enum

from sqlalchemy import create_engine
from sqlalchemy.orm import  Session

from bookkeeper.database.models import UserSchema, AuthorSchema, LibrarySchema, BookSchema, Base
from bookkeeper.database.dto import Book, Author, Library, User

BASE_DIR = "bookkeeper"
DB_NAME  = "bookkeeper.db"

class DBMessage(Enum):
    """Enum with possible messages from db"""
    CREATED = 1
    AUTHOR_NOT_FOUND = 2
    OBJECT_LIST = 3
    OBJECT = 4
    DELETED = 5
    BOOK_NOT_FOUND = 6
    MODIFIED = 7
    USER_NOT_FOUND = 8


class DBResponse:
    """A wrapper around DBMessage, it can additionally contntain response like an id or object"""
    def __init__(self, message: DBMessage, value = None):

        self.message = message
        if self.message in (
            DBMessage.OBJECT,
            DBMessage.OBJECT_LIST,
            DBMessage.CREATED,
            DBMessage.DELETED
        ):
            if value is None:
                raise ValueError("This DB message requires additional field - value")
            self.value = value
        else: self.value = None

    def __repr__(self):
        if self.value is not None:
            return self.value.__repr__()
        return self.message.__repr__()

    def __str__(self):
        if self.value is not None:
            return self.value.__str__()
        return self.message.__str__()

    def __json__(self):
        if self.message in (DBMessage.OBJECT, self.message == DBMessage.CREATED):
            return self.value.__json__()
        if self.message == DBMessage.OBJECT_LIST:
            return [obj.__json__() for obj in self.value]
        return None

    def __iter__(self):
        if self.message == DBMessage.OBJECT_LIST:
            return self.value.__iter__()
        raise ValueError("this response is not iterable")

class Database():
    """A class for interacting with the database"""

    def __init__(self):
        os.makedirs(os.path.join(os.getenv('APPDATA'),BASE_DIR), exist_ok=True)

        if sys.platform.startswith('win'):
            path = f"sqlite:///{os.path.join(os.getenv('APPDATA'), BASE_DIR, DB_NAME)}"
        else:
            path = f"sqlite:///{os.path.join(
                os.path.expanduser("~"),
                ".config",
                BASE_DIR,
                DB_NAME
            )}"
        path = path.replace('\\', "/")

        self.engine = create_engine(path, echo=False)
        Base.metadata.create_all(self.engine)

    def add_book(self, book: Book) -> DBResponse:
        """Adds a book to the database"""
        if self.does_author_exist(book.author_id):
            session =  Session(bind = self.engine)
            book = book.db()
            session.add(book)
            session.commit()
            return DBResponse(DBMessage.CREATED, book.id)

        return DBResponse(DBMessage.AUTHOR_NOT_FOUND)

    def add_author(self, author: Author) -> DBResponse:
        """Adds author to the database"""
        session =  Session(bind = self.engine)
        author = author.db()
        session.add(author)
        session.commit()
        return DBResponse(DBMessage.CREATED, author.id)

    def add_user(self, user: User) -> DBResponse:
        """Adds user to the database"""
        session =  Session(bind = self.engine)
        user = user.db()
        session.add(user)
        session.commit()
        return DBResponse(DBMessage.CREATED, user.id)

    def add_library(self, library: Library) -> DBResponse:
        """adds library to the database"""
        session =  Session(bind = self.engine)
        library = library.db()
        session.add(library)
        session.commit()
        return DBResponse(DBMessage.CREATED, library.id)

    def get_books(self) -> DBResponse:
        """Returns all books from the database"""
        session =  Session(bind = self.engine)
        resp =  DBResponse(
            DBMessage.OBJECT_LIST,
            [Book.from_db(obj) for obj in session.query(BookSchema).all()]
        )
        session.close()
        return resp

    def get_authors(self) -> DBResponse:
        """Returns all authors from the database"""
        session =  Session(bind = self.engine)
        resp =  DBResponse(
            DBMessage.OBJECT_LIST,
            [Author.from_db(obj) for obj in session.query(AuthorSchema).all()]
        )
        session.close()
        return resp

    def get_users(self) -> DBResponse:
        """Returns all users from the database"""
        session =  Session(bind = self.engine)
        resp =  DBResponse(
            DBMessage.OBJECT_LIST,
            [User.from_db(obj) for obj in session.query(UserSchema).all()]
        )
        session.close()
        return resp

    def get_libraries(self) -> DBResponse:
        """Returns all libraries from the database"""
        session =  Session(bind = self.engine)
        resp = DBResponse(
            DBMessage.OBJECT_LIST,
            [Library.from_db(obj) for obj in session.query(LibrarySchema).all()]
        )
        session.close()
        return resp

    def get_library_by_id(self, library_id):
        """Returns library with matching id from the database"""
        session = Session(bind = self.engine)
        resp = DBResponse(
            DBMessage.OBJECT,
            Library.from_db(
                session.query(LibrarySchema).where(LibrarySchema.id == library_id).first()
            )
        )
        session.close()
        return resp

    def get_books_by_author_id(self, author_id) -> DBResponse:
        """Returns all the books from author with a given id"""
        session =  Session(bind = self.engine)
        books = session.query(AuthorSchema).where(AuthorSchema.id == author_id).first().books
        resp = DBResponse(
            DBMessage.OBJECT_LIST,
            [Book.from_db(obj) for obj in books]
        )
        session.close()
        return resp

    def get_books_by_user_id(self, user_id) -> DBResponse:
        """Returns all the books currently owned by the given user"""
        session =  Session(bind = self.engine)
        books = session.query(UserSchema).where(UserSchema.id == user_id).first().books
        resp = DBResponse(
            DBMessage.OBJECT_LIST,
            [Book.from_db(obj) for obj in books]
        )
        session.close()
        return resp

    def get_book_by_id(self, book_id: int) -> DBResponse:
        """Returns book with given id"""
        session = Session(bind = self.engine)
        resp = DBResponse(
            DBMessage.OBJECT,
            Book.from_db(session.query(BookSchema).where(BookSchema.id == book_id).first())
        )
        session.close()
        return resp

    def get_books_by_library(self, library_id : int) -> DBResponse:
        """Returns all the books from the library with a given id"""
        session =  Session(bind = self.engine)
        books = session.query(LibrarySchema).where(LibrarySchema.id == library_id).first().books
        resp = DBResponse(
            DBMessage.OBJECT_LIST,
            [Book.from_db(obj) for obj in books]
        )
        session.close()
        return resp

    def get_author_by_id(self, author_id: int) -> DBResponse:
        """Returns author with a given id"""
        session = Session(bind = self.engine)
        resp = DBResponse(
            DBMessage.OBJECT,
            Author.from_db(session.query(AuthorSchema).where(AuthorSchema.id == author_id).first())
        )
        session.close()
        return resp

    def get_user_by_id(self, user_id: int) -> DBResponse:
        """Returns user with a matching id from the database"""
        session = Session(bind = self.engine)
        resp = DBResponse(
            DBMessage.OBJECT,
            User.from_db(session.query(UserSchema).where(UserSchema.id == user_id).first())
        )
        return resp

    def does_author_exist(self, author_id:int) -> bool:
        """Checks if author with a given id exists in the database"""
        try:
            return self.get_author_by_id(author_id) is not None
        except AttributeError:
            return False

    def delete_book(self, book_id:int):
        """deletes a book with a given id"""
        session = Session(bind = self.engine)
        book = session.query(BookSchema).where(BookSchema.id == book_id).first()
        if book:
            session.delete(book)
            session.commit()
            return DBResponse(DBMessage.DELETED, id)
        return DBResponse(DBMessage.BOOK_NOT_FOUND)

    def edit_book(self, book_id, **options) -> DBResponse:
        """edits a book with a given id"""
        session = Session(bind = self.engine)
        book = session.query(BookSchema).where(BookSchema.id == book_id).first()
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

    def edit_user(self, user_id : int, **options) -> DBResponse:
        """edits user with a given id"""
        session = Session(bind = self.engine)
        user = session.query(UserSchema).where(UserSchema.id == user_id).first()

        if user:
            if 'name' in options:
                user.name = options["name"]
            if 'surname' in options:
                user.surname = options["surname"]

            session.commit()
            return DBResponse(DBMessage.MODIFIED)
        return DBResponse(DBMessage.USER_NOT_FOUND)

    def edit_author(self, author_id : int, **options):
        """edits author with a given id"""
        session = Session(bind = self.engine)
        author = session.query(AuthorSchema).where(AuthorSchema.id == author_id).first()

        if author:
            if 'name' in options:
                author.name = options["name"]
            if 'surname' in options:
                author.surname = options["surname"]

            session.commit()
            return DBResponse(DBMessage.MODIFIED)
        return DBResponse(DBMessage.AUTHOR_NOT_FOUND)
