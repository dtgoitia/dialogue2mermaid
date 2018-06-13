import json


def load_dialogue(path: str):
    with open(path) as fd:
        return json.load(fd)
