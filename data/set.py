import json
import urllib.request
import urllib.parse


def set_data(entity):
    for propertyStrict in entity["wikidata"]:
        property = "wd-"+str(propertyStrict)
        send_query(entity, property, entity["wikidata"][propertyStrict])


def set_alignment(entity):
    property = "wd-"+"wikidata-alignment"
    send_query(entity, property, entity["wikidata-alignment"])


def send_query(entity, property, value):
    print('https://histoiredelart.fr/api/data/item/set/' + str(entity["id"]) + '/' + property + '/' + urllib.parse.quote_plus(json.dumps(value)))
    response = urllib.request.urlopen(
        'https://histoiredelart.fr/api/data/item/set/' + str(entity["id"]) + '/' + property + '/' + urllib.parse.quote_plus(json.dumps(value)))
    # req.add_header('Content-Type', 'application/json')
    result = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))

    print(str(entity["id"])+": "+str(property)+" > "+str(result))


def full_set():
    with open('../content/data/new-entities.json') as json_data:
        entities = json.load(json_data)

    for id in entities:
        if "wikidata" in entities[id]:
            set_data(entities[id])
        if "wikidata-alignment" in entities[id]:
            set_alignment(entities[id])

full_set()