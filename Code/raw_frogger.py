'''
Use this frogger to obtain CoNLL-format of 
reclassified entity types
'''

import frog as f
from pprint import pprint
import sys
import argparse
import re
import json
import time
import format_data as fd
import reclassify as rc

#@profile
def main(data, dump):
    """
    Systematically frog a large data file containing
    JSON structures of lobby documents on each line
    """
    start_time = time.time()
    frogger = f.Frog(f.FrogOptions(parser=False, lemma=False, morph=False, chunking=False, mwu=True), "/etc/frog/frog.cfg")
    with open(data) as d:
        with open(dump, 'w') as out:
            text = d.read()
            raw_output = parse(text, frogger)
            reclassified = rc.reclassify(raw_output)
            reformatted = fd.reformat(reclassified)
            out.write(reformatted)
    
    print("--- %s seconds ---" % (time.time() - start_time))
     
      

def parse(text, frogger):
    """
    Frog the given document and return the result
    as a json dict
    """
    output = frogger.process_raw(text)
    return output

if __name__ == '__main__':

    p = argparse.ArgumentParser()
    p.add_argument('-data', type=str, help='path to data file with lobby documents that needs frogging', default='data/lobby/test')
    p.add_argument('-dump', type=str, help='path to the dump', default='data/lobby/test_output')

    args = p.parse_args(sys.argv[1:])

    main(args.data, args.dump)