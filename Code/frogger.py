import frog as f
from pprint import pprint
import sys
import argparse
import re
import json
import time
from collections import defaultdict
# from guppy import hpy


def main(data, dump):
    """
    Systematically frog a large data file containing
    JSON structures of lobby documents on each line
    """
    start_time = time.time()
    storage_dict = {}
    with open(data) as json_data:
        processed = 0
        for j in json_data:
            doc = json.loads(j)
            output = parse(doc)
            doc_id = doc['_id']
            storage_dict[doc_id] = {}
            storage_dict[doc_id]['information'] = {}
            storage_dict[doc_id]['entities'] = {}
            save_info(doc, storage_dict[doc_id]['information'])
            save_ne(output, storage_dict[doc_id]['entities'])
            processed += 1
            print("documents frogged so far:", processed)
            # h = hpy()
            # print("memory usage:", h.heap())
            if processed == 5:
                break;
    
    print("--- %s seconds ---" % (time.time() - start_time))

    # ## Write dictionary to file
    # with open(dump, 'w') as outfile:
    #     json.dump(storage_dict, outfile)        
            

    pprint(storage_dict)

def parse(doc):
    """
    Frog the given document and return the result
    as a json dict
    """
    text = doc['_source']['content']
    frogger = f.Frog(f.FrogOptions(parser=False, lemma=False, morph=False, chunking=False, mwu=True), "/etc/frog/frog.cfg")
    output = frogger.process(text)

    return output

def save_ne(sample, entity_dict):  
    """
    Save named entities from the sample that is frogged data
    """
    for token in sample:
        if contains_entity(token):
            ## Check if entity already dict
            entity = token['text']
            entity_type = token['ner']
            if entity not in entity_dict:
                entity_dict[entity] = {}
            ## Check if entity type already in dict
            if entity_type not in entity_dict[entity]:
                entity_dict[entity][entity_type] = 1
            ## Increase the count for this type
            entity_dict[entity][entity_type] += 1

def save_info(sample, info_dict):
    """
    Save meta information of lobby document.
    """
    info_dict['type'] = sample['_type']
    info_dict['source'] = sample['_source']['source_name']

def contains_entity(token):
    answer = False
    chunks = token['ner'].split('_')
    for chunk in chunks:
        if chunk != 'O':
            answer = True

    return answer

if __name__ == '__main__':

    p = argparse.ArgumentParser()
    p.add_argument('-data', type=str, help='path to data file with lobby documents that needs frogging', default='data/lobby/lobby_tiny.txt')
    p.add_argument('-dump', type=str, help='path to the dump', default='data/lobby/lobby_dump.txt')

    args = p.parse_args(sys.argv[1:])

    main(args.data, args.dump)