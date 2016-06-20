vote_file = 'data/lobby/train_entities_global'
gazetteer_file = 'data/lobby/gazetteer'

import json
import re
import operator
from collections import defaultdict

def reclassify(frogged_raw):
    with open(vote_file) as f:
        entities = json.load(f)
    with open(gazetteer_file) as g:
        gazetteer = json.load(g)
    reclassified_output = ''
    lines = frogged_raw.split('\n')
    for idx, line in enumerate(lines):
        if line.strip():
            splitted = line.split('\t')
            # keep token, POS-tag, and entity tag (BIO)
            token = splitted[1]
            pos = splitted[4]
            tag = splitted[6]
            if reclassifiable(token, tag, entities):           
                tag = lookup_type(token, tag, gazetteer)
                if not tag:
                    print("voting instead...")
                    tag = vote_type(token, splitted[6], entities)
            reclassified_output += (token + ' ' + pos + ' ' + tag + '\n')

    return reclassified_output

def lookup_type(token, tag, gazetteer):
    if token in gazetteer:
        new_type = gazetteer[token].strip()
        iob_chain = [re.sub('-\w*', '', iob) for iob in tag.split('_')]
        new_tag = ''
        for idx, iob in enumerate(iob_chain):
            if idx != len(iob_chain)-1:
                new_tag += (iob + '-' + new_type + '_')
            else:
                new_tag += (iob + '-' + new_type)
        print(token, tag, new_tag)
        return new_tag
    else:
        return False

def reclassifiable(token, tag, entities):
    return 'O' not in tag.split('_') and token in entities and token[0].isupper() 

def vote_type(token, tag, entities, confidence=0.7 ):
    if not reclassifiable(token, tag, entities):
        return tag
    counts = defaultdict(int)
    iob_chain = [re.sub('-\w*', '', iob) for iob in tag.split('_')]
    total = 0
    for iob in entities[token]:
        total += entities[token][iob]
        type_chain = re.sub('PRO|EVE', 'MISC', re.sub('.-', '', iob)) #for iob in t.split('_')
        counts[type_chain] += entities[token][iob]
    if max(counts.values())/float(total) > confidence:
        new_tag = ''
        max_type_chain = max(counts, key=counts.get).split('_')
        for idx, max_type in enumerate(max_type_chain):
            if idx != len(max_type_chain)-1:
                new_tag += (iob_chain[idx] + '-' + max_type + '_')
            else:
                new_tag += (iob_chain[idx] + '-' + max_type)
        if new_tag != tag:
            print(token, tag, new_tag)
        return new_tag
    return tag





