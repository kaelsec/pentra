import json
import yaml

def load_json(path: str):
    """
    Load a JSON file and return its content.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_yaml(path: str):
    """
    Load a YAML file and return its content (usually a list of dicts).
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_json(path: str, data):
    """
    Save a Python object to a JSON file with UTF-8 encoding.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
