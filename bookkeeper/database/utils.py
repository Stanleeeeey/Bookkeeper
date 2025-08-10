"""usefull functions to help database"""

def cast_to(arg, cast_to_type: type):
    "casts to type, returns none if impossible"
    try:
        return cast_to_type(arg)
    except TypeError:
        return None


def is_within_chr_limit(text: str, chr_limit: int):
    """checks if string is short enough"""
    return len(text)<=chr_limit
