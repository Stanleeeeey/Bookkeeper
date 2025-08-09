import json, os , sys

SETTING = "setting.json"
BASE_DIR = "bookkeeper"

class Settings:
    def __init__(self):

        f = open_settings()
        self.data = json.load(f)

    def __getitem__(self, key):
        return self.data[key]


def initialize_settings():
    os.makedirs(os.path.join(os.getenv('APPDATA'),BASE_DIR), exist_ok=True)

    if sys.platform.startswith('win'):
        path = f"{os.path.join(os.getenv('APPDATA'), BASE_DIR, SETTING)}"
            
    else:
        path = f"{os.path.join(os.path.expanduser("~"), ".config", BASE_DIR, SETTING)}"
    path = path.replace('\\', "/")
    f = open(path, "w")
    f.write("{}")

def open_settings():
    os.makedirs(os.path.join(os.getenv('APPDATA'),BASE_DIR), exist_ok=True)

    if sys.platform.startswith('win'):
        path = f"{os.path.join(os.getenv('APPDATA'), BASE_DIR, SETTING)}"
            
    else:
        path = f"{os.path.join(os.path.expanduser("~"), ".config", BASE_DIR, SETTING)}"

    path = path.replace('\\', "/")
    try: return open(path, "r+")
    except:
        initialize_settings()
        return open(SETTING, "r+")
    
def set_setting(key, value):
    f = open_settings()
    data = json.load(f)
    data[key] = value
    f.seek(0)
    f.write(json.dumps(data))
    f.truncate() 



def get_setting(key):

    f = open_settings()
    data = json.load(f)
    try: return data[key]
    except: return None

