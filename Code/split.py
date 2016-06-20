import json
from pprint import pprint
import random

## used to make the test set of the first 100 files
def split(infile, outfile, n=100):
    """
    Write out n documents to the outfile
    from the beginning
    """
    with open(infile, 'r') as f:
        with open(outfile, 'w') as out:
            i = 0
            for line in f:
                i += 1
                out.write(line)
                if i == n:
                    break

def generate_train_set(infile, outfile, n=1000):
    """
    Pick n random documents from the infile
    and write them to the outfile
    """
    with open(infile, 'r') as f:
        with open(outfile, 'w') as out:
            items = f.readlines()
            total_docs = len(items)
            random_items = random.sample(xrange(100, total_docs), n) ## 100 to avoid test set docs
            for item in random_items:
                out.write(items[item])



def get_text(infile, outfile):
    """
    Write only the text of the JSON 
    entries in the infile to the outfile
    """
    with open(infile) as json_data:
        with open(outfile, 'w') as out:
            for d in json_data:
                current = json.loads(d)
                out.write(current['_source']['content'].encode('utf-8') + '\n')

def get_type(doc_type, infile, outfile):
    """
    Keep the JSON format, but only write
    out specific doc types
    """
    with open(infile) as json_data:
        with open(outfile, 'w') as out:
            for d in json_data:
                current = json.loads(d)
                if current['_type'] == doc_type:
                    out.write(d)