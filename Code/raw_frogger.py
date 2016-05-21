import frog as f
from pprint import pprint
import sys
import argparse
import re
import json
import time
import format_data as fd

#@profile
def main(data, dump):
    """
    Systematically frog a large data file containing
    JSON structures of lobby documents on each line
    """
    start_time = time.time()
    frogger = f.Frog(f.FrogOptions(parser=False, lemma=False, morph=False, chunking=False, mwu=True), "/etc/frog/frog.cfg")
    with open(data) as json_data:
        with open(dump, 'w') as out:
            for j in json_data:
                try:
                    doc = json.loads(j)
                    raw_output = parse(doc, frogger)
                    filtered = fd.filter_output(raw_output)
                    reformatted = fd.reformat(filtered)
                    out.write(reformatted)
                except:
                    continue
    
    print("--- %s seconds ---" % (time.time() - start_time))
     
      

def parse(doc, frogger):
    """
    Frog the given document and return the result
    as a json dict
    """
    text = doc['_source']['content']
    output = frogger.process_raw(text)
    return output

def contains_entity(token):
    answer = False
    chunks = token['ner'].split('_')
    for chunk in chunks:
        if chunk != 'O':
            answer = True

    return answer

if __name__ == '__main__':

    p = argparse.ArgumentParser()
    p.add_argument('-data', type=str, help='path to data file with lobby documents that needs frogging', default='data/lobby/error_analysis_set.txt')
    p.add_argument('-dump', type=str, help='path to the dump', default='data/lobby/dumps/lobby_predicteda.txt')

    args = p.parse_args(sys.argv[1:])

    main(args.data, args.dump)