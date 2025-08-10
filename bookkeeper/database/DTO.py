"""To be able to return database objects and read them"""
from bookkeeper.database.models import AuthorSchema, BookSchema, LibrarySchema, UserSchema

class Author:
    """Data tranfer object for Author"""
    def __init__(self, name: str, surname: str, author_id = None):
        self.name= name
        self.surname = surname
        self.id = author_id

    def db(self) -> AuthorSchema:
        """converts DTO to db model"""
        return AuthorSchema(self.name, self.surname)

    @staticmethod
    def from_db(author: AuthorSchema):
        """creates Author from db model"""
        return Author(author.name, author.surname, author.id)

class User:
    """DTO object for user"""
    def __init__(self, name:str, surname: str, user_id = None):
        self.name = name
        self.surname = surname
        self.id = user_id

    def db(self) -> UserSchema:
        """converts DTO to db model"""
        return UserSchema(self.name, self.surname)

    @staticmethod
    def from_db(user: UserSchema):
        """creates User from db model"""
        return User(user.name, user.surname, user.id)

class Library:
    """DTO object for library"""
    def __init__(self,  name:str, owned_by: int, library_id = None, owner: User = None):
        self.id = library_id
        self.name = name
        self.owned_by = owned_by
        self.owner = owner

    def db(self) -> LibrarySchema:
        """converts DTO to db model"""
        return LibrarySchema(self.name, self.owned_by)

    @staticmethod
    def from_db(library: LibrarySchema):
        """creates Library from db model"""
        return Library(
            name = library.name,
            owned_by=User.from_db(library.user).id,
            library_id= library.id,
            owner = User.from_db(library.user)
        )

class Book:
    """DTO object for book"""

    def __init__(self, title : str, author_id : int, edition: int, status : int, library_id : Library, user_id, user: User = None, book_id = None, author: Author = None, library: Library = None):
        self.id = book_id
        self.title = title
        self.author = author
        self.author_id = author_id
        self.edition = edition
        self.status = status
        self.library_id = library_id
        self.user = user
        self.user_id = user_id
        self.library = library

    def db(self) -> BookSchema:
        """converts DTO to db model"""
        return BookSchema(
            title= self.title,
            author_id= self.author_id,
            status = self.status,
            library_id=self.library_id,
            edition=self.edition,
            held_by=self.user_id
        )

    @staticmethod
    def from_db(book: BookSchema):
        """creates Book from db model"""
        return Book(
            title = book.title,
            author_id = book.author.id,
            edition = book.edition,
            status = book.status,
            library = Library.from_db(book.library),
            library_id=book.library.id,
            user = User.from_db(book.user),
            user_id = book.held_by,
            book_id = book.id,
            author = Author.from_db(book.author)
        )
