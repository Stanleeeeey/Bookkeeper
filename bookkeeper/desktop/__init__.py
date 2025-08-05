import webview
from flask import Flask
from threading import Thread
from bookkeeper.desktop.views import landing_page


class Route:
    def __init__(self, action, **kwargs):
        self.action = action
        self.kwargs = kwargs

    def __call__(self, **kwargs):

        return self.action(**kwargs, **self.kwargs)

class DesktopApp:
    def __init__(self, api_url= ""):
        self.api_url = api_url

    def run(self, ):

        self.server = Flask(__name__, static_folder='./static', template_folder='./templates')
        self.server.add_url_rule("/", "", Route(landing_page))

        #self.server.run()
        webview.create_window('Bookkeeper', self.server)
        webview.start(debug = True)