import os
import json


CONFIG_FILE = os.path.join(os.path.dirname(__file__), "settings.json")


def save_settings(settings):
    with open(CONFIG_FILE, "w") as f:
        json.dump(settings, f)


def load_settings():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}
