
from bookkeeper.database.models import *

class Author:
    def __init__(self, name: str, surname: str, id = None):
        self.name= name
        self.surname = surname
        self.id = id

    def db(self) -> AuthorSchema:
        return AuthorSchema(self.name, self.surname)
    
    def from_db(author: AuthorSchema):
        return Author(author.name, author.surname, author.id)

class User:
    def __init__(self, name:str, surname: str, id = None):
        self.name = name
        self.surname = surname
        self.id = id

    def db(self) -> UserSchema:
        return UserSchema(self.name, self.surname)
    
        
    def from_db(user: UserSchema):
        if user: return User(user.name, user.surname, user.id)

class Library:
    def __init__(self,  name:str, owned_by: User, id = None):
        self.id = id
        self.name = name
        self.owned_by = owned_by

    
    def db(self) -> LibrarySchema:
        return LibrarySchema(self.name, self.owned_by.id)
    
    def from_db(library: LibrarySchema):
        return Library(library.name, User.from_db(library.user), library.id)
    

class Book:
    def __init__(self, title : str, author : Author, edition: int, status : int, library : Library, used_by: User, id = None):
        self.id = id
        self.title = title
        self.author = author
        self.edition = edition
        self.status = status
        self.library = library
        self.used_by = used_by

    def db(self) -> BookSchema:
        return BookSchema(self.title, self.author.id, self.status, self.library.id, self.edition)
    
        
    def from_db(book: BookSchema):
        return Book(book.title, book.author, book.edition, book.status, Library.from_db(book.library), User.from_db(book.user), book.id)