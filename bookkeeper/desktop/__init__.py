import webview
from flask import Flask
from threading import Thread
from bookkeeper.desktop.views import *


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
        self.server.add_url_rule("/", "", Route(landing_page))
        self.server.add_url_rule("/home", "home", Route(home, db = self.db))
        self.server.add_url_rule("/create-main-user", "create main user", Route(create_main_user_page, db = self.db), methods = ["GET", "POST"])
        self.server.add_url_rule("/create-library", "create library", Route(create_library, db = self.db), methods = ["GET", "POST"])
        self.server.add_url_rule("/library/<id>", "get library", Route(library, db = self.db))

    def run(self, ):
        self.db = Database()
        self._initialize_server()

        self.server.run()


        webview.create_window('Bookkeeper', self.server)
        #webview.start(debug = True)