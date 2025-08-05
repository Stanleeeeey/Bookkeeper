from bookkeeper.database.database import Database
from flask import request, Response



def get_arg(arg_name: str, cast_to :type = str):
    try:
        ans = request.args[arg_name]
    except: return None
    try:
        return cast_to(ans)
    except:
        return None
