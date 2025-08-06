
from bookkeeper.database import Book
from bookkeeper.database.database import DBMessage
from bookkeeper.api.utils import *
from flask import  Response



def index():
    
    return "API Welcome page"

def get_books(db):
    return db.get_books().__json__()

def get_book_by_id(id, db):
    return db.get_book_by_id(id, ).__json__()

def get_books_by_author_id(id, db):
    return db.get_books_by_author_id(id).__json__()

def get_authors(db):
    return db.get_authors().__json__()


def add_book(db, ):
    title =get_arg("title", )
    if not title: return Response(response = "title is invalid or missing", status = 400)

    author_id = get_arg("author_id", cast_to = int)
    if not author_id: return Response(response = "author_id is invalid or missing", status = 400)

    status = get_arg("status",  cast_to = int)
    if not status: return Response(response = "status is invalid or missing", status = 400)
    
    edition = get_arg("edition",  cast_to = int)
    if not edition: return Response(response = "edition is invalid", status = 400)
    
    resp = db.add_book(Book(title = title, author_id = author_id, status = status,edition = edition))
    if resp.message == DBMessage.CREATED:
        return Response(response = f'{resp.value}', status = 200)
    else:
        return Response(response = f"Bad request DB error code : {resp.message}", status = 400)

    