from bookkeeper.desktop.settings import get_setting
from flask import render_template, request

def render_page(template, **kwargs):
    mode = get_setting("mode", "light")
    return render_template(template, mode= mode, **kwargs)

def get_arg(arg_name: str, cast_to :type = str):
    try:
        ans = request.args[arg_name]
    except: return None
    try:
        return cast_to(ans)
    except:
        return None