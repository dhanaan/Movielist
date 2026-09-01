import json
from pathlib import Path

APP_DIR = Path.home() / ".Movielist"

def ensure_dir_exist():
    APP_DIR.mkdir(exist_ok=True)

def write(path, data):
    ensure_dir_exist()
    with open(APP_DIR/path, 'w') as file:
        json.dump(data, file)

def read(path):
    try:
        with open(APP_DIR/path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return None
    except FileNotFoundError:
        write(APP_DIR/path, [])
        return None
