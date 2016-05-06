
def model(text):
    model = []
    with open(text, 'r') as t:
        for line in t:
            if line.strip():
                model.append(line.split(' '))
    return model

def evaluate(processed, correct):
    total_tokens = len(correct)
    correct_pos = 0
    recalled_entities = 0
    correct_predictions = 0
    correct_entities = 0
    total_entities = 0
    error_cases = []
    c = 0 ## line difference correction for processed text
    i = 0
    j = 0
    while j < total_tokens:
        processed_entry = processed[i+c]
        correct_entry = correct[j]
        identical = True

        ## If tokens differ, find correct mapping
        if processed_entry[0] != correct_entry[0]:
            c = equalize(processed, correct, i, j)

        ## Check POS equality
        if processed_entry[1] == correct_entry[1]:
            correct_pos += 1
        else:
            identical = False

        ## Check if entity detected in processed text
        if processed_entry[2] != 'O\n':
            recalled_entities += 1

        ## Check if entity detected in correct text
        if correct_entry[2] != 'O\n':
            total_entities += 1

        ## Check prediction equality
        if processed_entry[2] == correct_entry[2]:
            correct_predictions += 1
        else:
            identical = False

        ## Check entity equality
        if processed_entry[2] != 'O\n' and correct_entry[2] != 'O\n' and processed_entry[2] == correct_entry[2]:
            correct_entities += 1

        if not identical:
            error_cases.append([processed_entry, correct_entry])

        i += 1
        j += 1

    results = []
    pos_acc = correct_pos/float(total_tokens)
    acc = correct_predictions/float(total_tokens)
    p = correct_entities/float(recalled_entities)
    r = recalled_entities/float(total_entities)
    f1 = (p*r)/(p+r)*2
    results.append(('POS-accuracy', pos_acc))
    results.append(('entity_accuracy', acc))
    results.append(('entity_precision', p))
    results.append(('entity_recall', r))
    results.append(('F1-score', f1))


    return results, error_cases 

def equalize(first, second, i, j):
    """
    Return index difference of the same
    token pair. This issue happens when
    some words are spread out over multiple entries
    or chunked together on one.
    """
    context = 100
    correction = 0
    target = second[j]

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

processed = model('data/conll/testa_reformatted.txt')
correct = model('data/conll/ned.testa.txt')
results, error_cases = evaluate(processed, correct)
for result in results:
    print result

# for i in range(0, 20):
#     print error_cases[i][0]
#     print error_cases[i][1], '\n'