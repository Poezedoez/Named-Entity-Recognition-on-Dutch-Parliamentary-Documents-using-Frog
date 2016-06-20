import json
from pprint import pprint
from collections import defaultdict
from operator import itemgetter

def count_doc_types(data, dump):
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

def count_unique_entities(test_set):
    entity_counter = defaultdict(int)
    with open(test_set) as t:
        for line in t:
            try:
                tokens = line.split(' ')
                if tokens[2] != 'O\n':
                    entity_counter[tokens[0]] += 1
            except:
                continue
    print len(entity_counter)

def sort_entities(data, dump):
    with open(data) as file:
        entities = json.load(file)

    occurrences = defaultdict(int)
    for entity in entities:
        for entity_type in entities[entity]:
            occurrences[entity] += entities[entity][entity_type]
    
    with open(dump, 'w') as out:
        for entity in sorted(occurrences, key=occurrences.get, reverse=True):
            out.write(entity.encode('utf-8') + '\t' + 'misc' + '\n')

