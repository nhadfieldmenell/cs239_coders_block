"""Simple library to return string.punctuation with the _ token removed.
"""

import string

def punctuation_no_underscore():
    punc = ''
    for i in string.punctuation:
        if i != '_':
            punc += i
    return punc
