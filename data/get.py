import json
import urllib.parse
import urllib.request
from pprint import pprint


def get_data_get_all():
    with open('content/data/entities.json') as json_data:
        entities = json.load(json_data)
    return entities
