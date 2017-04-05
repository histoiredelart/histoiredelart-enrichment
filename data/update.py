import json
import urllib.parse
import urllib.request


def update_data_update_all_items():
    response = urllib.request.urlopen(
        'https://histoiredelart.fr/api/data/items/get/all/TMatFYOroGkaxxgGaC3t045IKzvNHd')
    result = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    print(result)

    with open('content/data/entities.json', 'w') as outfile:
        json.dump(result, outfile)


