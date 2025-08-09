import json

SETTING_URL = "setting.json"

def initialize_settings():
    f = open(SETTING_URL, "w")
    f.write("{}")

def open_settings():
    try: return open(SETTING_URL, "r+")
    except:
        initialize_settings()
        return open(SETTING_URL, "r+")

class Settings:
    def __init__(self):

        f = open_settings()
        self.data = json.load(f)

    def __getitem__(self, key):
        return self.data[key]

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

