import xml.etree.ElementTree
import urllib.request
import urllib.parse


def getCommons(file_name):
    response = urllib.request.urlopen(
        'https://tools.wmflabs.org/magnus-toolserver/commonsapi.php?image='+urllib.parse.quote(file_name.replace(' ', '_'))+'&thumbwidth=400&languages=fr')

    result = response.read().decode(response.info().get_param('charset') or 'utf-8')
    e = xml.etree.ElementTree.fromstring(result)

    thumbnail400 = []
    thumbnailFull = []
    urlCommon = []

    for i in e.findall('file'):
        for ii in i.findall('urls'):
            for iii in ii.findall('file'):
                thumbnailFull.append(iii.text)
            for iii in ii.findall('description'):
                urlCommon.append(iii.text)
            for iii in ii.findall('thumbnail'):
                thumbnail400.append(iii.text)

    # print(thumbnailFull)
    # print(urlCommon)
    # print(thumbnail400)
    return {'data-enrichment-thumbnail-400': thumbnail400, 'data-enrichment-url-common': urlCommon, 'data-enrichment-thumbnail-full': thumbnailFull}