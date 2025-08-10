"""WARNING: this module is NOT USED. Support for it will be added in the future"""

from flask import Flask, request

from bookkeeper.api.routes import *

class Route:
    def __init__(self, action, **kwargs):
        self.action = action
        self.kwargs = kwargs

    def __call__(self, **kwargs):

        return self.action(**kwargs, **self.kwargs)

class API:
    def __init__(self, db):
        self.db = db

        self.app = Flask(__name__)
        
    def run(self):
        self.app.add_url_rule("/", "", Route(index))
        self.app.add_url_rule("/get_books", "get_books", Route(get_books, db = self.db))
        self.app.add_url_rule("/get_book_by_id/<id>", "get_book_by_id", Route(get_book_by_id, db = self.db))
        self.app.add_url_rule("/get_books_by_author_id/<id>", "get_books_by_author_id", Route(get_books_by_author_id, db = self.db))
        self.app.add_url_rule("/get_authors", "get_authors", Route(get_authors, db = self.db))


        self.app.add_url_rule("/add_book", "add_book", Route(add_book, db = self.db), methods = ["POST"])
        self.app.run()
