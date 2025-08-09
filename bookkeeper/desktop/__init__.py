import webview
from flask import Flask
from bookkeeper.desktop.routes import *


class Route:
    def __init__(self, action, **kwargs):
        self.action = action
        self.kwargs = kwargs

    def __call__(self, **kwargs):

        return self.action(**kwargs, **self.kwargs)

class DesktopApp:
    def __init__(self, api_url= ""):
        self.api_url = api_url

    def _initialize_server(self):
        self.server = Flask(__name__, static_folder='./static', template_folder='./templates')
        self.server.add_url_rule("/","", Route(landing_page))
        self.server.add_url_rule("/home", "home", Route(home, db = self.db))
        self.server.add_url_rule("/create-main-user", "create main user", Route(add_main_user, db = self.db), methods = ["GET", "POST"])
        self.server.add_url_rule("/add-user", "add user", Route(add_user, db = self.db), methods = ["GET", "POST"])
        self.server.add_url_rule("/edit-user/<id>", "edit user", Route(edit_user, db  =self.db), methods = ["GET", "POST"])
        self.server.add_url_rule("/create-library", "create library", Route(add_library, db = self.db), methods = ["GET", "POST"])
        self.server.add_url_rule("/add-book/<id>", "add book", Route(add_book, db = self.db), methods = ["GET", "POST"])
        self.server.add_url_rule("/add-author/<id>", "add author", Route(add_author, db = self.db), methods = ["GET", "POST"])
        self.server.add_url_rule("/settings", "settings", Route(settings), methods = ["GET", "POST"])
        self.server.add_url_rule("/edit-book/<id>", "edit book", Route(edit_book, db  =self.db), methods = ["GET", "POST"])
        self.server.add_url_rule("/edit-author/<id>", "edit author", Route(edit_author, db  =self.db), methods = ["GET", "POST"])
        self.server.add_url_rule("/change-setting", "change setting", Route(change_setting), methods = ["POST"])
        self.server.add_url_rule("/library/<id>", "get library", Route(library, db = self.db))
        self.server.add_url_rule("/author/<id>", "get author", Route(author, db = self.db))
        self.server.add_url_rule("/book/<id>", "get book", Route(book, db = self.db))
        self.server.add_url_rule("/manage-users", "manage users", Route(users, db = self.db))
        self.server.add_url_rule("/user/<id>", "user", Route(user, db = self.db))


    def run(self, ):
        self.db = Database()
        self._initialize_server()

        webview.create_window('Bookkeeper', self.server, min_size=(600, 600))        
        webview.start(icon = "static/assets/banner-light.png")