"""
Format frog input and output
Don't try to make sense of this code;
it's not good for your health.
"""
import re

def filter_output(frogged_raw):
    """
    Format frogged text by throwing away unwanted output.
    """
    filtered_output = ''
    lines = frogged_raw.split('\n')
    for line in lines:
        splitted = line.split('\t')
        # keep token, POS-tag, and entity tag (BIO) 
        try:
            filtered_output += (splitted[1] + ' ' + splitted[4] + ' ' + splitted[6] + '\n')
        except:
            continue

    return filtered_output

def format_input(conll_text, outfile):
    """
    Format conll input to its original tekst.
    """
    with open(conll_text, 'r') as infile:
        sentences = []
        sentence = []
        for line in infile:
            sample = line.split(' ')
            sentence.append(sample[0])
            if re.match('[.!:?]', line):
                sentences.append(sentence)
                sentence = []

        with open(outfile, 'w') as out:           
            for sentence in sentences:
                for word in sentence:
                    out.write(word + ' ')
                out.write('\n')

## onderstaande code is echt jammer
def reformat(frog_filtered):
    """
    Reformat frogged text to match exact
    format of conll-2002, including same POS_tags.
    """
    formatted_output = ''
    lines = frog_filtered.split('\n')
    for line in lines:
        try:
            if line.strip():
                splitted = line.split(' ')
                ## dechunk words if chunked on same line
                if '_' in splitted[0]:
                    entries = split_chunk(splitted)
                    formatted_output += entries
                # reformat POS-tag by stripping additional info and changing type
                else: 
                    old_tag = splitted[1].split('(')[0]
                    new_tag = replace(old_tag)
                    formatted_output += (splitted[0] + ' ' + new_tag + ' ' + splitted[2] + '\n') 
                    #formatted_output += (splitted[0] + ' ' + new_tag + '\n')
        except:
            continue

    return formatted_output

def split_chunk(chunk):
    """
    Split a chunk of words
    concatenated with '_'
    into string of 1 word per line.
    """
    tokens = chunk[0].split('_')
    pos = chunk[1].split('_')
    entities = chunk[2].split('_')
    entries = ''
    for i in range(0, len(tokens)):
        entries += tokens[i] + ' ' + replace(pos[i]) + ' ' + entities[i] + '\n'
        #entries += tokens[i] + ' ' + replace(pos[i]) + '\n'

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

format_input('data/lobby/lobby_test.txt', 'data/lobby/lobby_test_textonly.txt')