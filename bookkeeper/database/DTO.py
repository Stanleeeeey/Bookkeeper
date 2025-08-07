
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
    def __init__(self,  name:str, owned_by: int, id = None, owner: User = None):
        self.id = id
        self.name = name
        self.owned_by = owned_by
        self.owner = owner

    
    def db(self) -> LibrarySchema:
        return LibrarySchema(self.name, self.owned_by)
    
    def from_db(library: LibrarySchema):
        return Library(library.name, owned_by=User.from_db(library.user).id, id = library.id, owner = User.from_db(library.user))
    

class Book:
    def __init__(self, title : str, author_id : int, edition: int, status : int, library_id : Library, user: User = None, user_id = None, id = None, author: Author = None, library: Library = None):
        self.id = id
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
        return BookSchema(self.title, self.author_id, self.status, self.library_id, self.edition, held_by=self.user_id)
    
        
    def from_db(book: BookSchema):
        return Book(
            title = book.title,
            author_id = book.author.id,
            edition = book.edition,
            status = book.status,
            library = Library.from_db(book.library),
            library_id=book.library.id,
            user = User.from_db(book.user),
            user_id = book.held_by,
            id = book.id,
            author = Author.from_db(book.author)
        )