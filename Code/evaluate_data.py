import sys
import argparse
from collections import defaultdict

def main(predicted, correct, e=0):
    """
    Print various evaluation metrics
    of the performance of Frog. Also
    prints @e error cases.
    """
    predicted_model = model(predicted)
    correct_model = model(correct)
    counts, error_cases, confusion = get_counts(predicted_model, correct_model)
    results = get_results(counts)

    for key, result in results.iteritems():
        print key, '%.2f'%result 

    for key, value in confusion.iteritems():
        for v, count in value.iteritems():
            print '%s predicted as %s %d times'%(key, v, count)

    for i in range(0, e):
        print error_cases[i][0]
        print error_cases[i][1], '\n'

def model(path):
    """
    Return the space seperated
    tokens of each line in the file
    as a list of tuples
    """
    model = []
    with open(path, 'r') as f:
        for line in f:
            if line.strip():
                model.append(line.split(' '))
    return model

def get_counts(predicted, correct):
    counts = defaultdict(int)
    counts['total_tokens'] = len(correct)
    error_cases = []
    confusion = {}
    a = 0 ## line difference correction for predicted text
    i = 0
    j = 0

    while j < counts['total_tokens']:
        try:
            predicted_entry = predicted[i+a] ## Default is same line, unless new alignment needed
            correct_entry = correct[j]

            ## If tokens differ, find correct mapping/alignment
            if predicted_entry[0] != correct_entry[0]:
                a = align(predicted, correct, i, j, counts)

            count_pos(predicted_entry, correct_entry, counts)
            identical, confusion = count_ner(predicted_entry, correct_entry, counts, confusion)
            
            if not identical:
                error_cases.append([predicted_entry, correct_entry])

            i += 1
            j += 1

        except:
            print 'Incorrect format on line %d'%j
            i += 1
            j += 1

    return counts, error_cases, confusion

def align(first, second, i, j, counts):
    """
    Return index difference of the same
    token pair. This issue happens when
    some words are spread out over multiple entries
    or chunked together on one.
    """
    context = 100
    correction = 0
    target = second[j]
    counts['equalizations'] += 1

    for h in range(1, context):
        ## look h entries ahead
        token_ahead = first[i+h]
        if token_ahead == target:
            correction = h
            break;

        ## look h entries back
        token_back = first[i-h]
        if token_back == target:
            correction = -h
            break;
        
    return correction

def count_pos(predicted_entry, correct_entry, counts):

    if predicted_entry[1] == correct_entry[1]:
        counts['correct_pos'] += 1
    else:
        if predicted_entry[1] == 'UNKNOWN':
            counts['unknown'] += 1

def count_ner(predicted_entry, correct_entry, counts, confusion):

    identical = True

    ## Check if relevant entity in predicted text is found
    if predicted_entry[2] != 'O\n' and correct_entry[2] != 'O\n':
        counts['recalled_entities'] += 1

    ## Check if entity found in correct text
    if correct_entry[2] != 'O\n':
        counts['total_entities'] += 1

    ## Check prediction equality
    if predicted_entry[2] == correct_entry[2]:
        counts['correct_predictions'] += 1
    else:
        identical = False

    ## Check whole entity equality
    if predicted_entry[2] != 'O\n' and correct_entry[2] != 'O\n' and predicted_entry[2] == correct_entry[2]:
        counts['correct_entities'] += 1

    ## Check IOB specific equality
    if predicted_entry[2] != 'O\n' and correct_entry[2] != 'O\n':
        predicted_iob = predicted_entry[2].split('-')[0]
        correct_iob = correct_entry[2].split('-')[0]
        if predicted_iob == correct_iob:
            counts['correct_iob_tags'] += 1

    ## Check type specific equality
    if predicted_entry[2] != 'O\n' and correct_entry[2] != 'O\n':
        predicted_type = predicted_entry[2].split('-')[1].rstrip()
        correct_type = correct_entry[2].split('-')[1].rstrip()
        if predicted_type == correct_type:
            counts['correct_types'] += 1
        ## Add to confusion matrix dict
        if correct_type not in confusion:
            confusion[correct_type] = defaultdict(int)
        confusion[correct_type][predicted_type] += 1

    return identical, confusion

def get_results(counts):
    """
    Return a results dict with different
    performance measures, such as precision,
    recall, and f1 all calculated with the accumulated counts
    """

    results = defaultdict(int)

    pos_acc = counts['correct_pos']/float(counts['total_tokens']-counts['unknown']) ## debatable whether conll POS tags are correct
    acc = counts['correct_predictions']/float(counts['total_tokens']) ## tells us tokens aren't tagged randomly as entities
    p = counts['correct_entities']/float(counts['recalled_entities']) ## tells us how precise the entity was assigned for IOB tag + type
    p_iob = counts['correct_iob_tags']/float(counts['recalled_entities']) ## tells us how precise the entity was assigned for IOB tag only
    p_type = counts['correct_types']/float(counts['recalled_entities']) ## tells us how precise the entity was assigned for type only
    r = counts['recalled_entities']/float(counts['total_entities']) ## how many named entities that were in text have actually been found
    f1 = (p*r)/(p+r)*2 ## harmonic mean between precision and recall


    results['POS-accuracy'] = pos_acc
    results['accuracy'] = acc
    results['precision'] = p
    results['IOB-precision'] = p_iob
    results['type-precision'] = p_type
    results['recall'] = r
    results['F1-score'] = f1

    return results    

if __name__ == '__main__':

    p = argparse.ArgumentParser()
    p.add_argument('-predicted', type=str, help='path to predicted test set', default='data/lobby/lobby_test_predicted.txt')
    p.add_argument('-correct', type=str, help='path to correct test set', default='data/lobby/lobby_test.txt')
    p.add_argument('-e', type=int, help='total error cases to print', default= 0)


    args = p.parse_args(sys.argv[1:])

    main(args.predicted, args.correct, args.e)