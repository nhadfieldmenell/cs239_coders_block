"""
    Iterate through all the questions and answers to generate a dict mapping term to its entropy value.
    Store the dict in entropies.pkl.
    Force every string to lower case for consistency.
    abc_def -> abcdef
    <code>self.data[seas_no][ep_no]['attribute'] -> self data seasno epno attribute
    ignore tokens that are just numbers (for storage size purposes)
"""
import string
import csv
import re
from collections import defaultdict
from collections import Counter

class EntropyCalculator:
    def __init__(self):
        self.term2count = defaultdict(int)
        self.term2discussion2count = {}
        self.questions_fn = '../pythonquestions/Questions.csv'
        self.answers_fn = '../pythonquestions/Answers.csv'
        self.tags_fn = '../pythonquestions/Tags.csv'

    
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
        #print body
        body = re.sub('<.*?>', '', body).lower()
        #print ''
        body = re.sub('\n|\r|/|\(|\)|\.|\[|\]', ' ', body)
        #print body
        occurrence = Counter(body.translate(None, string.punctuation).split())
        #print occurrence
        #print ''
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
        with open(in_fn, 'rb') as infile:
            reader = csv.reader(infile)
            count = 0
            for line in reader:
                count += 1
                if count == 1:
                    continue
                if count > 40:
                    break
                if questions:
                    discussion_id, _, _, _, _, body = line
                else:
                    _, _, _, discussion_id, _, body = line
                self.parse_terms(body, discussion_id)

        print self.term2count
        print ''
        print self.term2discussion2count
        exit(1)


    def count_terms(self):
        """Iterate through all discussions (questions & answers) to count the occurrences of terms.
        
        Update term2count and term2discussion2count.
        """
        self.process_csv()
        print ''
        self.process_csv(questions=False)



def main():
    e = EntropyCalculator()
    e.count_terms()


if __name__ == '__main__':
    main()


