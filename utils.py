import json
import os


def get_json(json_path) -> dict:
    f = open(json_path, "r")
    s = json.load(f)
    f.close()
    return s
