"""
    Iterate through all the questions and answers to generate a dict mapping term to its entropy value.
    Store the dict in entropies.pkl.
    Force every string to lower case for consistency.
    abc_def -> abcdef
    <code>self.data[seas_no][ep_no]['attribute'] -> self data seasno epno attribute
    ignore tokens that are just numbers (for storage size purposes)
        this includes, say, version numbers: '10.5' -> '' -> ignored
"""
import pickle
import string
import csv
import re
import math
import time
from collections import defaultdict
from collections import Counter

class EntropyCalculator:
    def __init__(self):
        self.term2count = defaultdict(int)
        self.term2discussion2count = {}
        self.questions_fn = '../pythonquestions/Questions.csv'
        self.answers_fn = '../pythonquestions/Answers.csv'
        self.tags_fn = '../pythonquestions/Tags.csv'
        self.discussions = set()
        self.term2entropy = defaultdict(float)

    #TODO: assert term2count has same # of terms as term2discussion2count


    def calc_entropies(self):
        """Calculate the entropy of each term and write a {term: entropy} dict to pickle.

        Call after self.count_terms()
        Note that we do -= instead of how the paper does +=.
        """
        num_discussions = float(len(self.discussions))
        num_terms = len(self.term2count)
        count = 0
        cur_time = time.time()
        for term in self.term2discussion2count:
            count += 1
            if count % (num_terms / 10) == 0:
                print 'calculated entropies for chunk %d of 10 in %.2fs' % (count / (num_terms/10), time.time() - cur_time)
                cur_time = time.time()
            term_ct = float(self.term2count[term])
            for discussion in self.term2discussion2count[term]:
                term_dis_ct = float(self.term2discussion2count[term][discussion])
                p_d = term_dis_ct / term_ct
                self.term2entropy[term] -= p_d * math.log(p_d, num_discussions)
        cur_time = time.time()

        with open('../pythonquestions/term2entropy.pkl', 'wb') as outfile:
            pickle.dump(self.term2entropy, outfile)
        print 'took %.2fs to dump pickle' % (time.time() - cur_time)

        zero_ents = []
        for term in self.term2entropy:
            entropy = self.term2entropy[term]
            if entropy:
                continue
                print '%s: %.3f' % (term, entropy)
            else:
                zero_ents.append(term)
        print 'zeros'
        print len(zero_ents)
        print 'total terms'
        print len(self.term2entropy)


    def inc_term2dis(self, term, discussion, val=1):
        """Increment term2discussion2count[term][discussion]. Initialize if necessary.

        Args:
            term: A string term.
            discussion: The int id of the discussion containing the term.
            val: The amount to increment by.
        """
        if term not in self.term2discussion2count:
            self.term2discussion2count[term] = defaultdict(int)
        self.term2discussion2count[term][discussion] += val


    def parse_terms(self, body, discussion):
        """Parse a question/answer body to update term2count and term2discussion2count.

        Args:
            body: A string containing a question/answer body.
            discussion: The int id of the discussion whose body we are parsing.
        """
        body = re.sub('\n|\r|/|\(|\)|\.|\[|\]|<.*?>', ' ', body).lower()
        occurrence = Counter(body.translate(None, string.punctuation).split())
        for term in occurrence:
            if term.isdigit():
                continue
            self.term2count[term] += occurrence[term]
            self.inc_term2dis(term, discussion, occurrence[term])


    def process_csv(self, questions=True):
        """Count the occurrences of terms in each document of a question/answer csv file.

        Args:
            questions: True if processing Questions.csv. False if processing Answers.csv.
        """
        in_fn = self.questions_fn if questions else self.answers_fn
        cur_time = time.time()
        with open(in_fn, 'rb') as infile:
            reader = csv.reader(infile)
            count = 0
            for line in reader:
                count += 1
                if count == 1:
                    continue
                if count % 10000 == 0:
                    print count
                    print 'time to process 10000: %.2f' % (time.time()-cur_time)
                    cur_time = time.time()
                if questions:
                    discussion_id, _, _, _, _, body = line
                else:
                    _, _, _, discussion_id, _, body = line
                discussion_id = int(discussion_id)
                self.discussions.add(discussion_id)
                self.parse_terms(body, discussion_id)
        print 'read %d lines' % count



    def count_terms(self):
        """Iterate through all discussions (questions & answers) to count the occurrences of terms.
        
        Update term2count, term2discussion2count, and discussions.
        """
        self.process_csv()
        self.process_csv(questions=False)
        return
        print self.term2count
        print ''
        print self.term2discussion2count



def main():
    e = EntropyCalculator()
    e.count_terms()
    e.calc_entropies()


if __name__ == '__main__':
    main()


