from enrichment.commons import getCommons
from data.wikidata import get_qwd
import json
import urllib.parse
import urllib.request
from parameters import hda_key

def enrichment(entity, wikidata, accepted_properties, get_entity):
    enrichment = {}

    if len(get_property(wikidata, "labels")) > 0:
        enrichment["label"] = get_property(wikidata, "labels")
    if len(get_property(wikidata, "aliases")) > 0:
        enrichment["aliases"] = get_property(wikidata, "aliases")
    if len(get_property(wikidata, "descriptions")) > 0:
        enrichment["descriptions"] = get_property(wikidata, "descriptions")

    claims = wikidata["claims"]
    for accepted_property in accepted_properties:
        if accepted_property == "P18":
            # P18 == Image
            if get_claim(claims, accepted_property, get_entity) is not None and "value" in get_claim(claims, accepted_property, get_entity) and get_claim(claims, accepted_property, get_entity)["value"] is not None:
                if type(get_claim(claims, accepted_property, get_entity)["value"]) is dict or type(
                        get_claim(claims, accepted_property, get_entity)["value"]) is list or type(
                        get_claim(claims, accepted_property, get_entity)["value"]) is object:
                    for url in get_claim(claims, accepted_property, get_entity)["value"]:
                        # print(url)
                        listCommons = getCommons(url)
                        for image in listCommons:
                            enrichment[image] = listCommons[image]
                        # print(enrichment)
                else:
                    url = get_claim(claims, accepted_property, get_entity)["value"]
                    # print(url)
                    listCommons = getCommons(url)
                    for image in listCommons:
                        enrichment[image] = listCommons[image]
                    # print(enrichment)
        if get_claim(claims, accepted_property, get_entity) is not None:
            # All other properties
            enrichment[accepted_property] = get_claim(claims, accepted_property, get_entity)

    entity['wikidata'] = enrichment
    return entity


def get_property(element, property):
    values = {}
    if property in element:
        if "fr" in element[property]:
            values["fr"] = element[property]["fr"]
        if "en" in element[property]:
            values["en"] = element[property]["en"]
    return values


def get_claim(claims, accepted_property, get_entity):
    returned_value = None
    if accepted_property in claims:
        value = []
        for iterate in claims[accepted_property]:
            if "qualifiers" in iterate:
                qualifiers = iterate["qualifiers"]
            else:
                qualifiers = None

            if "mainsnak" in iterate and "datavalue" in iterate["mainsnak"] and "datatype" in iterate["mainsnak"]:
                if iterate["mainsnak"]["datatype"] == "string":
                    value.append({"mainsnak": iterate["mainsnak"]["datavalue"]["value"], "qualifiers": qualifiers})
                elif iterate["mainsnak"]["datatype"] == "wikibase-item":
                    property_json_value = get_entity(iterate["mainsnak"]["datavalue"]["value"]["id"])
                    labels_value = get_property(property_json_value, "labels")
                    value.append({"mainsnak": {"labels": labels_value, "value": iterate["mainsnak"]["datavalue"]["value"]["id"]}, "qualifiers": qualifiers})
                elif iterate["mainsnak"]["datatype"] == "time":
                    value.append({"mainsnak": iterate["mainsnak"]["datavalue"]["value"], "qualifiers": qualifiers})
                elif iterate["mainsnak"]["datatype"] == "globe-coordinate":
                    value.append({"mainsnak": iterate["mainsnak"]["datavalue"]["value"], "qualifiers": qualifiers})
                elif iterate["mainsnak"]["datatype"] == "quantity":
                    unit_qwd = None
                    unit_labels = None
                    if "unit" in iterate["mainsnak"]["datavalue"]["value"]:
                        unit_qwd = get_qwd(iterate["mainsnak"]["datavalue"]["value"]["unit"])
                        if unit_qwd is not None:
                            property_json_value = get_entity(unit_qwd)
                            unit_labels = get_property(property_json_value, "labels")
                    value.append({"mainsnak": {"amount": iterate["mainsnak"]["datavalue"]["value"]["amount"], "unit": {"qwd": unit_qwd, "labels": unit_labels}}, "qualifiers": qualifiers})

        property_json = get_entity(accepted_property)
        labels = get_property(property_json, "labels")
        returned_value = {"labels": labels, "value": value}
    return returned_value


def properties():
    response = urllib.request.urlopen(
        'https://histoiredelart.fr/api/data/property/get/wikidata/' + hda_key())
    return json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
