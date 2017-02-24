"""
    Iterate through all the questions and answers to generate a dict mapping term to its entropy value.
    Store the dict in entropies.pkl.
    Force every string to lower case for consistency.
    abc_def -> abcdef
    <code>self.data[seas_no][ep_no]['attribute'] -> self data seasno epno attribute
    ignore tokens that are just numbers (for storage size purposes)
        this includes, say, version numbers: '10.5' -> '' -> ignored
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
        self.discussions = set()

    
    def calc_entropies(self):
        num_discussions = len(self.discussions)


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
        body = re.sub('<.*?>', '', body).lower()
        body = re.sub('\n|\r|/|\(|\)|\.|\[|\]', ' ', body)
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
                discussion_id = int(discussion_id)
                self.discussions.add(discussion_id)
                self.parse_terms(body, discussion_id)



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


