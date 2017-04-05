import json
from data.get import get_data_get_all
from data.update import update_data_update_all_items
from enrichment.property import enrichment
from enrichment.property import properties
from data.wikidata import get_entity
from data.wikidata import get_qwd
from alignment.items import alignment

# update_data_update_all_items()

entities = get_data_get_all()
countEnrichments = 0
countAlignments = 0

for id in entities:
    print(id)
    if "sameAs" in entities[id]:
        for sameAs in entities[id]["sameAs"]:
            qwd = get_qwd(sameAs)
            if qwd is not None:
                break

        wikidata_entity = None
        if qwd is not None:
            wikidata_entity = get_entity(qwd)
            entity = enrichment(entities[id], wikidata_entity, properties(), get_entity)
            print("Enrichment: " + str(entities[id]))
            countEnrichments += 1
        else:
            print(str(entities[id])+": No Qwd")
    elif "wikidata-alignment" not in entities[id]:
        entities[id] = alignment(entities[id])
        print("Alignment: " + str(entities[id]))
        countAlignments += 1

with open('content/data/new-entities.json', 'w') as outfile:
    json.dump(entities, outfile)

print("Enrichments: "+str(countEnrichments))
print("Aligmnents: "+str(countAlignments))
