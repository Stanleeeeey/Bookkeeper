import json

SETTING_URL = "setting.json"



def set_setting(key, value):
    f = open(SETTING_URL, "r+")
    data = json.load(f)
    data[key] = value
    f.seek(0)
    f.write(json.dumps(data))
    f.truncate() 

def get_setting(key, backup = None):
    f = open(SETTING_URL, "r+")
    data = json.load(f)
    try: return data[key]
    except: return backup