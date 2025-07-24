import json
import os

def get_config_path():
    return os.path.join(os.path.dirname(__file__), "..", "config.json")

def save_config(data: dict):
    with open(get_config_path(), "w") as f:
        json.dump(data, f, indent=4)

def load_config() -> dict:
    path = get_config_path()
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)