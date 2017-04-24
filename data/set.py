import json
import urllib.request
import urllib.parse
import requests
from parameters import hda_key_set


def set_data(entity, entities, count):
    for propertyStrict in entity["wikidata"]:
        property = "wd-"+str(propertyStrict)
        send_query(entity, property, entity["wikidata"][propertyStrict], entities, count)


def set_alignment(entity, entities, count):
    send_query(entity, "wikidata-alignment", entity["wikidata-alignment"], entities, count)


def send_query(entity, property, value, entities, count):
    print("Set -> "+str("{:.1%}".format(count/len(entities)))+" | "+str(entity["id"]) + ": " + str(property) + " > " + str(value))

    r = requests.post("https://histoiredelart.fr/api/data/item/set/"+hda_key_set(),
                  data={'entity_id': entity["id"], 'property': property, 'value': json.dumps(value)})
    print("Set -> "+str("{:.1%}".format(count/len(entities)))+" | "+str(r.status_code), r.reason)
    # print(r.text[:300] + '...')


def reset_data_entity(entity_id, entities, count):
    print("Set -> "+str("{:.1%}".format(count/len(entities)))+" | "+"reset: "+str(entity_id))
    r = requests.post("https://histoiredelart.fr/api/data/item/reset/"+hda_key_set(),
                  data={'entity_id': entity_id})
    print("Set -> "+str("{:.1%}".format(count/len(entities)))+" | "+str(r.status_code), r.reason)
    # print(r.text[:300] + '...')


def full_set():
    with open('../content/data/new-entities.json') as json_data:
        entities = json.load(json_data)

    count = 0
    for id in entities:
        reset_data_entity(id, entities, count)

        if "wikidata" in entities[id]:
            set_data(entities[id], entities, count)
        if "wikidata-alignment" in entities[id]:
            set_alignment(entities[id], entities, count)
        count += 1
full_set()