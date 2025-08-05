from flask import render_template
from bookkeeper.desktop.settings import get_setting

def landing_page():
    mode = get_setting("mode", "light")
    return render_template("launch.html", mode= mode)