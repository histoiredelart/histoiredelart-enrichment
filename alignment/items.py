# Objectif de ce script : identifier les items Wikidata qui pourraient matcher avec des items DATA
from data.wikidata import search_entity


def alignment(entity):
    query = ""
    if "label" in entity:
        query += str(entity["label"])
    if "creator" in entity:
        if query != "":
            query += " "
        query += str(entity["creator"])

    if query != "":
        response = search_entity(entity["label"])

        if "search" in response and len(response["search"]) > 0:
            entity["wikidata-alignment"] = []
            for item in response["search"]:
                entity["wikidata-alignment"].append(item)
    return entity
