"""A library of utility functions used to generate a query.
"""

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
        word_frequency: A list of tuples (x, y) such that:
            x: A word.
            y: The word's frequency in the code context.
        term2entropy: A dict mapping a strin term to its entropy value.

    Returns:
        The same word_frequency list with typos pruned and frequencies added to their counterparts.

    Example:
        input: [('what', .5), ('whit', .1), ('blah', .4)
        output: [('what', .6), ('blah', .4)]
    '''
    pass
