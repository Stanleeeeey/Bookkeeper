"""Usefull functions to reduce boilerplate in routes.py"""
from flask import render_template, request

from bookkeeper.desktop.settings import get_setting

def render_page(template, **kwargs):
    """a wrapper arounf render_template.
    Adds additional information about user preferred mode and previous page"""

    mode = get_setting("dark-mode", )
    go_back = get_arg("go_back")

    return render_template(template, mode= "dark" if mode else "light", go_back = go_back, **kwargs)

def get_arg(arg_name: str, cast_to :type = str):
    """gets arg from te url"""

    ans = request.args.get(arg_name)
    if ans is None:
        return None
    try:
        return cast_to(ans)
    except TypeError:
        return None