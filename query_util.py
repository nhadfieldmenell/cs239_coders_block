"""A library of utility functions used to generate a query.
"""

from collections import defaultdict
from Levenshtein import distance

def levenshtein(a, b):
    '''Compute the Levenshtein distance between two strings.

    Args:
        a: A string.
        b: A string.

    Returns:
        The int levenshtein distance between the two.
    '''
    return distance(a, b)

def prune_typos(word_frequency, term2entropy):
    '''Prune out words whose Levenshtein distance == 1 according to alg in paper.

    Args:
        word_frequency: A list of lists [x, y] such that:
            x: A word.
            y: The word's frequency in the code context.
        term2entropy: A dict mapping a strin term to its entropy value.

    Returns:
        The same word_frequency list with typos pruned and frequencies added to their counterparts.

    Example:
        input: [['what', .5], ['whit', .1], ['blah', .4]]
        output: [['what', .6], ['blah', .4]]
    '''
    len2words = defaultdict(list)
    for word, frequency in word_frequency:
        len2words[len(word)].append([word, frequency])

    keys = sorted(len2words.keys())
    for key_i in range(len(keys)):
        length = keys[key_i]
        word_freqs = len2words[length]
        pops = set()
        pops_next = set()

        for i in range(len(word_freqs)):
            for j in range(i+1, len(word_freqs)):
                if levenshtein(word_freqs[i][0], word_freqs[j][0]) == 1:
                    if word_freqs[i][1] > word_freqs[j][1]:
                        word_freqs[i][1] += word_freqs[j][1]
                        pops.add(j)

                    elif word_freqs[i][1] < word_freqs[j][1]:
                        word_freqs[j][1] += word_freqs[i][1]
                        pops.add(i)

                    else:
                        if term2entropy[word_freqs[i][0]] > term2entropy[word_freqs[j][0]]:
                            word_freqs[i][1] += word_freqs[j][1]
                            pops.add(j)

                        else:
                            word_freqs[j][1] += word_freqs[i][1]
                            pops.add(i)

            if key_i == len(keys) - 1 or keys[key_i+1] != length + 1:
                continue

            word_freqs_next = len2words[length+1]
            for j in range(len(word_freqs_next)):
                if levenshtein(word_freqs[i][0], word_freqs_next[j][0]) == 1:
                    if word_freqs[i][1] > word_freqs_next[j][1]:
                        word_freqs[i][1] += word_freqs_next[j][1]
                        pops_next.add(j)
                        
                    elif word_freqs[i][1] < word_freqs_next[j][1]:
                        word_freqs_next[j][1] += word_freqs[i][1]
                        pops.add(i)

                    else:
                        if term2entropy[word_freqs[i][0]] > term2entropy[word_freqs[j][0]]:
                            word_freqs[i][1] += word_freqs_next[j][1]
                            pops_next.add(j)

                        else:
                            word_freqs[j][1] += word_freqs[i][1]
                            pops.add(i)

        for pop in reversed(sorted(pops)):
            word_freqs.pop(pop)

        if pops_next:
            for pop in reversed(sorted(pops_next)):
                len2words[length+1].pop(pop)

    word_freq = []
    for length in len2words:
        for i in len2words[length]:
            word_freq.append(i)

    return word_freq





            



    pass
