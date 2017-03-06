from __future__ import division

'''
    Using the generated code context and term to entropy dictionary, this script ranks
    the terms in the context based on a term quality index (TQI):
        TQI_t = v_t * (1 - E_t)
    where t is the term, v_t is the frequency in the context, and E_t is its entropy.
    Once the raking is complete, the Query Generation Service will select the top n terms
    to devise a query.

    This script will return the top n terms as a query, where n is specified by the user.
'''

import pickle
import time
from collections import Counter
import operator
# import query_util

def generate_query(code_context, term2entropy, n):
    TQI = {}
    func_calls = code_context['func_calls']
    freqs = Counter(func_calls)
    for func_call in func_calls:
        v_t = freqs[func_call]
        E_t = term2entropy[func_call] if term2entropy[func_call] != 0 else 1
        TQI[func_call] = v_t * (1 - E_t)
    sorted_TQI = reversed(sorted(TQI.items(), key=operator.itemgetter(1)))
    query = []
    for i in sorted_TQI:
        if n == 0:
            return query
        else:
            query.append(i[0])
            n -= 1

    return query

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', help='Number of terms in the query', required=True)
    args = parser.parse_args()
    code_context = pickle.load(open('code_context.pkl', 'rb'))
    term2entropy = pickle.load(open('term2entropy.pkl', 'rb'))

    cur_time = time.time()
    query = generate_query(code_context, term2entropy, int(args.number))
    print 'took %.2fs to generate query' % (time.time() - cur_time)
    print query

    cur_time = time.time()
    with open('query.pkl', 'wb') as outfile:
        pickle.dump(query, outfile)
    print 'took %.2fs to dump pickle' % (time.time() - cur_time)
