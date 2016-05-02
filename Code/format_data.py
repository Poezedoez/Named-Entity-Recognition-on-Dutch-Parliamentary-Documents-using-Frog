"""
Format frog input and output
"""
import re

def filter_output(frogged_text, outfile):
    """
    Format frog input by throwing away unwanted output.
    """
    with open(frogged_text, 'r') as infile:
        with open(outfile, 'w') as out:
            for line in infile:
                splitted = line.split('\t')
                # keep token, POS-tag, and entity tag (BIO) 
                try:
                    out.write(splitted[1] + ' ' + splitted[4] + ' ' + splitted[6] + '\n')
                except:
                    continue

def format_input(conll_text, outfile):
    """
    Format conll input to its original tekst.
    """
    with open(conll_text, 'r') as infile:
        sentences = []
        sentence = []
        for line in infile:
            if line != '\n':
                sample = line.split(' ')
                sentence.append(sample[0])
            else:
                sentences.append(sentence)
                sentence = []

        with open(outfile, 'w') as out:           
            for sentence in sentences:
                for word in sentence:
                    out.write(word + ' ')
                out.write('\n')

## onderstaande code is echt jammer
def reformat(formatted_text, outfile):
    """
    Reformat frogged text to match exact
    format of conll-2002, including same POS_tags.
    """
    with open(formatted_text, 'r') as infile:
        with open(outfile, 'w') as out:
            for line in infile:
                if line.strip():
                    splitted = line.split(' ')
                    ## frog tends to chunk words together in the same line
                    if '_' in splitted[0]:
                        entries = split_chunk(splitted)
                        out.write(entries)
                    # reformat POS-tag by stripping additional info and changing type
                    else: 
                        old_tag = splitted[1].split('(')[0]
                        new_tag = replace(old_tag)
                        out.write(splitted[0] + ' ' + new_tag + ' ' + splitted[2]) 

def split_chunk(chunk):
    tokens = chunk[0].split('_')
    pos = chunk[1].split('_')
    entities = chunk[2].split('_')
    entries = ''
    for i in range(0, len(tokens)):
        entries += tokens[i] + ' ' + replace(pos[i]) + ' ' + entities[i] + '\n'

    return entries

def replace(tag):
    """
    Replace POS-tag returning conll-2002
    notation instead of the frog notation
    """
    replace_dict = {}
    replace_dict['N'] = 'N'
    replace_dict['BW'] = 'Adv'
    replace_dict['LID'] = 'Art'
    replace_dict['ADJ'] = 'Adj'
    replace_dict['VZ'] = 'Prep'
    replace_dict['WW'] = 'V'
    replace_dict['VG'] = 'Conj'
    replace_dict['LET'] = 'Punc'
    replace_dict['TW'] = 'Num'
    replace_dict['VNW'] = 'Pron'

    try:
        return replace_dict[tag]
    except:
        return 'UNKNOWN'

# filter_output('data/conll/testa_frogged.txt', 'data/conll/testa_filtered.txt')
# filter_output('data/conll/testb_frogged.txt', 'data/conll/testb_filtered.txt')
reformat('data/conll/testa_filtered.txt', 'data/conll/testa_reformatted.txt')
reformat('data/conll/testb_filtered.txt', 'data/conll/testb_reformatted.txt')
#reformat('data/conll/conll_frogged.txt', 'data/conll/conll_frogged_reannotated.txt')