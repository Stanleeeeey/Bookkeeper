"""Modify and read settings from bookkeeper.json"""
import json
import os
import sys

if sys.platform.startswith('win'):
    os.makedirs(os.path.join(os.getenv('APPDATA'),"bookkeeper"), exist_ok=True)
    PATH = os.path.join(os.getenv('APPDATA'), "bookkeeper", "bookkeeper.json")
    PATH = PATH.replace("\\", "/")
else:
    os.makedirs(os.path.join(os.path.expanduser("~"), ".config", "bookkeeper"), exist_ok=True)
    PATH = os.path.join(os.path.expanduser("~"), ".config", "bookkeeper", "bookkeeper.json")
    PATH = PATH.replace("\\", "/")

class Settings:
    """class to store user settings"""
    def __init__(self):

        f = open_settings()
        self.data = json.load(f)

    def __getitem__(self, key):
        return self.data[key]


def initialize_settings():
    """creates an empty json file"""
    f = open(PATH, "w", encoding= "utf-8")
    f.write("{}")

def open_settings():
    """opens setting files and initializes empty if does not exist"""
    try:
        return open(PATH, "r+", encoding= "utf-8")
    except OSError:
        initialize_settings()
        return open(PATH, "r+", encoding = "utf-8")

def set_setting(key, value):
    """sets key to given value"""
    f = open_settings()
    data = json.load(f)
    data[key] = value
    f.seek(0)
    f.write(json.dumps(data))
    f.truncate()

def get_setting(key):
    """returns a value from given key"""
    f = open_settings()
    data = json.load(f)

    return data.get(key)
