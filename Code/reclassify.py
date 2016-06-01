vote_file = 'data/lobby/lobby_train_total_entities.txt'
import json
import re
import operator
from collections import defaultdict

def reclassify(frogged_raw):
    with open(vote_file) as f:
        entities = json.load(f)
    reclassified_output = ''
    lines = frogged_raw.split('\n')
    for idx, line in enumerate(lines):
        if line.strip():
            splitted = line.split('\t')
            # keep token, POS-tag, and entity tag (BIO)
            token = splitted[1]
            pos = splitted[4]
            iob = splitted[6]
            if contains_entity(iob) and token in entities and token[0].isupper():
                iob = vote_type(token, iob, entities)
            reclassified_output += (token + ' ' + pos + ' ' + iob + '\n')

    return reclassified_output

def vote_type(token, iob, entities, confidence=0.7):
    counts = defaultdict(int)
    current_iob = iob.split('-')[0]
    total = 0
    for t in entities[token]:
        total += entities[token][t]
        # entity_type = t.split('-')[1].split('_')[0]
        counts[t] += entities[token][t]
    if max(counts.values())/float(total) > confidence and max(counts, key=counts.get) != iob:
        # print('voted', token, iob, 'to', current_iob + '-' + entity_type)
        # return current_iob + '-' + entity_type
        print('voted', token, iob, 'to', max(counts, key=counts.get))
        return max(counts, key=counts.get)
    return iob

def contains_entity(iob):
    answer = False
    chunks = iob.split('_')
    for chunk in chunks:
        if chunk != 'O':
            answer = True

    return answer

