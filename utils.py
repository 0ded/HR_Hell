import json
import os


def get_json(json_path) -> dict:
    f = open(json_path, "r")
    s = json.load(f)
    f.close()
    return s


def write_json(json_path, dict: dict):
    with open(json_path, "w") as f:
        json.dump(dict, f)
    f.close()

