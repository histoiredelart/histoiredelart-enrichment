import re
import json
import urllib.parse
import urllib.request


def get_qwd(url):
    qwd = None

    if re.search('https://www\.wikidata\.org/entity/', url):
        qwd = url.replace('https://www.wikidata.org/entity/', "")
    elif re.search('http://www\.wikidata\.org/entity/', url):
        qwd = url.replace('http://www.wikidata.org/entity/', "")
    elif re.search('https://www\.wikidata\.org/wiki/', url):
        qwd = url.replace('https://www.wikidata.org/wiki/', "")
    elif re.search('http://www\.wikidata\.org/wiki/', url):
        qwd = url.replace('http://www.wikidata.org/wiki/', "")

    return qwd


def get_entity(qwd):
    if qwd is not None:
        response = urllib.request.urlopen(
            'http://www.wikidata.org/w/api.php?action=wbgetentities&ids='+qwd+'&format=json')
        result = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))['entities'][qwd]
        return result
    else:
        return None


def search_entity(query):
    try:
        response = urllib.request.urlopen(
            'https://www.wikidata.org/w/api.php?action=wbsearchentities&search=' + urllib.parse.quote(
                str(query)) + '&limit=20&language=fr&format=json')
        result = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    except urllib.error.URLError as e:
        print(e.reason)
        result = None
    except UnicodeEncodeError:
        print("There was an error encrypting...")
        result = None
    except IsADirectoryError:
        print("There was an error for directory...")
        result = None
    except ConnectionResetError:
        print("Connection reset by peer ...")
        result = None
    except TimeoutError:
        print("TimeoutError ...")
        result = None

    return result


def get_parent_classes(entity):
    returned_classes = {}
    if "claims" in entity:
        # Nature de l'élément
        if "P31" in entity["claims"]:
            returned_classes["P31"] = entity["claims"]["P31"]
        # Sous-classe de
        if "P279" in entity["claims"]:
            returned_classes["P279"] = entity["claims"]["P279"]

    if len(returned_classes) > 0:
        return returned_classes
    else:
        return None


def is_child_of(entity, parent, level, level_max):
    if level <= level_max:
        parent_classes = get_parent_classes(entity)
        returned_value = None

        if parent_classes is not None:
            for id in parent_classes:
                for parent_class in parent_classes[id]:
                    if parent_class['mainsnak']['datavalue']['value']['id'] == parent:
                        returned_value = parent_class['mainsnak']['datavalue']['value']['id']
                        break
                    else:
                        if level < level_max:
                            is_child_of(get_entity(parent_class['mainsnak']['datavalue']['value']['id']), parent,
                                        level+1, level_max)

        return returned_value
    else:
        return False

