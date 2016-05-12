import json
from pprint import pprint

def analyze(data, dump):
    type_counter = {}
    with open(data) as json_data: 
        for d in json_data:
            current = json.loads(d)
            doc_type = current['_type']
            if doc_type not in type_counter:
                type_counter[doc_type] = 1
            else:
                type_counter[doc_type] += 1

    with open(dump, 'w') as outfile:
        json.dump(type_counter, outfile)

analyze('data/lobby/lobby_unzipped.txt', 'data/lobby/dumps/type_count.txt')