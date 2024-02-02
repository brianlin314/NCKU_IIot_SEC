import json


def get_variable():
  with open('config.json', 'r') as f:
    config = json.load(f)
    return config