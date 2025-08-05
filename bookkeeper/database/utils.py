


def cast_to(arg, type: type):
    try:
        return type(arg)
    except:
        return 0


def is_within_chr_limit(text: str, chr_limit: int):
    return len(text)<=chr_limit