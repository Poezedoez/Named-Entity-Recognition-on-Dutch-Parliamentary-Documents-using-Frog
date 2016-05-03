import json
from pprint import pprint

def split(infile, outfile, n=1):
    """
    Write out n documents to the outfile
    """
    with open(infile, 'r') as data_file:
        with open(outfile, 'w') as out:
            i = 0
            for line in data_file:
                i += 1
                out.write(line)
                if i == n:
                    break


#split('data/lobby/lobby_unzipped.txt', 'data/lobby/lobby_tiny.txt', 10)

def get_text(infile, outfile):
    with open(infile) as json_data:
        with open(outfile, 'w') as out:
            for d in json_data:
                current = json.loads(d)
                out.write(current['_source']['content'].encode('utf-8') + '\n')

get_text('data/lobby/lobby_tiny.txt', 'lobby_tiny_text.txt')