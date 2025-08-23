import os
import json


CONFIG_FILE = os.path.join(os.path.dirname(__file__), "settings.json")

CONFIG = dict()


def save_settings(settings):
    with open(CONFIG_FILE, "w") as f:
        json.dump(settings, f)


def load_settings():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            CONFIG.update(json.load(f))
    return CONFIG
