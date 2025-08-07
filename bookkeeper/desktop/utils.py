from bookkeeper.desktop.settings import get_setting
from flask import render_template, request

def render_page(template, **kwargs):
    mode = get_setting("dark-mode", False)
    go_back = get_arg("go_back")
    
    return render_template(template, mode= "dark" if mode else "light", go_back = go_back, **kwargs)

def get_arg(arg_name: str, cast_to :type = str):
    try:
        ans = request.args[arg_name]
    except: return None
    try:
        return cast_to(ans)
    except:
        return None