def enrichment(entity, wikidata, accepted_properties, get_entity):
    enrichment = {}

    if len(get_property(wikidata, "labels")) > 0:
        enrichment["label"] = get_property(wikidata, "labels")
    if len(get_property(wikidata, "aliases")) > 0:
        enrichment["aliases"] = get_property(wikidata, "aliases")
    if len(get_property(wikidata, "description")) > 0:
        enrichment["description"] = get_property(wikidata, "description")

    claims = wikidata["claims"]
    for accepted_property in accepted_properties:
        if get_claim(claims, accepted_property, get_entity) is not None:
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
            if "mainsnak" in iterate and "datavalue" in iterate["mainsnak"]:
                if iterate["mainsnak"]["datavalue"]["type"] == "string":
                    value.append(iterate["mainsnak"]["datavalue"]["value"])
                elif iterate["mainsnak"]["datavalue"]["type"] == "wikibase-entityid":
                    property_json_value = get_entity(iterate["mainsnak"]["datavalue"]["value"]["id"])
                    labels_value = get_property(property_json_value, "labels")
                    value.append({"labels": labels_value, "value": iterate["mainsnak"]["datavalue"]["value"]["id"]})
                elif iterate["mainsnak"]["datavalue"]["type"] == "time":
                    value.append(iterate["mainsnak"]["datavalue"]["value"])

        property_json = get_entity(accepted_property)
        labels = get_property(property_json, "labels")

        returned_value = {"labels": labels, "value": value}

    return returned_value

def properties():
    return {
        "P17": "Pays",
        "P18": "Image",
        "P19": "Lieu de naissance",  # Pour les agents
        "P20": "Lieu de décès",  # Pour les agents
        "P21": "Sexe ou genre",  # Pour les agents
        "P22": "Père",  # Pour les agents
        "P25": "Mère",  # Pour les agents
        "P26": "Epoux",  # Pour les agents
        "P27": "Pays de nationalité",  # Pour les agents
        "P31": "Nature de l'élément",
        "P84": "Architecte",
        "P88": "Commanditaire",
        "P101": "Domaine d'activité",  # Pour les agents, peut rejoindre le style ou l'occupation
        "P106": "Occupation",  # Pour les agents, cad profession
        "P108": "Employer",  # Pour les agents, peut rejoindre la notion de mécène
        "P112": "Fondé par",  # Edifice
        "P119": "Lieu de sépulture",  # Pour les agents
        # "P127": "Propriétaire", Inutile si systématiquement Etat Français
        "P131": "Localisation administrative",
        "P135": "Mouvement",
        "P136": "Genre",
        "P140": "Religion",  # Utile en archi religieuse
        "P144": "Basé sur",  # Source d'inspiration (mythe, etc)
        "P149": "Style architectural",  # Utile en archi religieuse
        "P170": "Creator",
        "P180": "Dépeint",
        "P186": "Matériau",
        "P195": "Collection",
        "P214": "VIAF ID",
        "P217": "Numéro d'inventaire",
        "P245": "ULAN ID",
        "P268": "BNF ID",
        "P269": "Identifiant IdRef, Sudoc",
        "P276": "Lieu (où se situe)",
        "P347": "Identifiant Joconde",
        "P373": "Catégorie Commons",
        "P380": "Identifiant Mérimée",
        "P495": "Pays d'origine",
        "P551": "Résidence",  # Pour les agents, cad villes où il a vécu
        "P569": "Date de naissance",  # Pour les agents
        "P570": "Date de décès",  # Pour les agents
        "P571": "Date de fondation/Création",
        # "P608": "Historique des expositions", Pas forcément intéressant pour le moment
        "P625": "Coordonnées géographiques",
        "P706": "Localisation géographique",
        "P708": "Diocèse",  # Utile pour l'archi religieuse
        "P727": "Europeana ID",
        "P735": "Prénom",  # Pour les agents
        # "P793" : "Evènement clé", Difficile à gérer pour le moment
        "P800": "Oeuvre notable",  # Pour les agents, pas forcément intéressant
        "P802": "Etudiants notables",  # Pour les agents
        "P825": "Dédicataire",  # Utile pour l'archi religieuse
        "P856": "Site officiel",
        "P935": "Galerie Commons",  # Voir la diff avec P373
        "P937": "Lieu de travail",  # Pour les agents
        "P973": "Décrit à l'URL",
        "P1066": "Elève de",  # Pour les agents
        "P1071": "Lieu de fabrication",
        "P1212": "Identifiant Atlas",
        "P1412": "Langue parlée",  # Pour les agents
        "P1435": "Statut patrimonial",  # A voir si intéressant
        "P1476": "Titre dans langue originelle",
        "P1477": "Nom de naissance",  # Pour les agents
        "P1559": "Nom dans la langue maternelle",  # Pour les agents
        "P1705": "Nom dans langue originelle",
        "P1962": "Mécène",  # Pour les agents
        "P2048": "Hauteur",
        "P2049": "Largeur",
        "P2344": "AGORHA ID",
        "P3373": "Frère ou soeur",  # Pour les agents
        "P3749": "Google Map ID"  # Utile pour les édifices
    }
