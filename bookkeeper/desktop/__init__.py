"""Running the desktop application"""
import webview
from flask import Flask

from bookkeeper.database.database import Database
from bookkeeper.desktop.routes import launch_page, home_page, add_author_page, add_book_page, add_library_page, add_main_user_page, add_user_page, author_page, book_page, change_setting, edit_author_page, edit_book_page, edit_user_page, library_page, settings_page, user_page, users_page


class Route:
    """Wrapper to accomadate additional arguments to routes functions"""
    def __init__(self,url, endpoint, action, methods = None, **kwargs):
        self.url = url
        self.endpoint = endpoint
        self.action = action
        self.kwargs = kwargs
        if methods is None:
            self.methods = ["GET"]
        else:
            self.methods = methods

    def __call__(self, **kwargs):

        return self.action(**kwargs, **self.kwargs)

class DesktopApp:
    """Class taking care of a deskotp application"""

    def __init__(self, api_url= ""):
        self.api_url = api_url

        self.db = Database()
        self.server = Flask(__name__, static_folder='./static', template_folder='./templates')

        #information about every desktop endpoint
        self.routes = [
            Route(
                "/",
                "",
                launch_page
            ),
            Route(
                "/home",
                "home",
                home_page,
                db = self.db
            ),
            Route(
                "/create-main-user",
                "create main user",
                add_main_user_page,
                db = self.db,
                methods = ["GET", "POST"]
            ),
            Route(
                "/add-user",
                "add user",
                add_user_page,
                methods = ["GET", "POST"],
                db = self.db
            ),
            Route(
                "/edit-user/<user_id>",
                "edit user",
                edit_user_page,
                methods = ["GET", "POST"],
                db  =self.db
            ),
            Route(
                "/create-library",
                "create library",
                add_library_page,
                methods = ["GET", "POST"],
                db = self.db
            ),
            Route(
                "/add-book/<library_id>",
                "add book", add_book_page,
                methods = ["GET", "POST"],
                db = self.db
            ),
            Route(
                "/add-author",
                "add author",
                add_author_page,
                methods = ["GET", "POST"],
                db = self.db
            ),
            Route(
                "/settings",
                "settings",
                settings_page,
                methods = ["GET", "POST"]
            ),
            Route(
                "/edit-book/<book_id>",
                "edit book",
                edit_book_page,
                methods = ["GET", "POST"],
                db  =self.db
            ),
            Route(
                "/edit-author/<author_id>",
                "edit author",
                edit_author_page,
                methods = ["GET", "POST"],
                db  =self.db
            ),
            Route(
                "/change-setting",
                "change setting",
                change_setting,
                methods = ["POST"]
            ),
            Route(
                "/library/<library_id>",
                "get library",
                library_page,
                db = self.db
            ),
            Route(
                "/author/<author_id>",
                "get author",
                author_page,
                db = self.db
            ),
            Route(
                "/book/<book_id>",
                "get book", 
                book_page,
                db = self.db
            ),
            Route(
                "/manage-users",
                "manage users",
                users_page,
                db = self.db
            ),
            Route(
                "/user/<user_id>",
                "user",
                user_page,
                db = self.db
            )
        ]

    def _initialize_server(self):

        for route in self.routes:
            self.server.add_url_rule(
                route.url,
                route.endpoint,
                route,
                methods = route.methods
            )
   
    def run(self, ):
        """Starts and runs the app"""
        self._initialize_server()

        webview.create_window('Bookkeeper', self.server, min_size=(600, 600))
        webview.start(icon = "static/assets/banner-light.png")
