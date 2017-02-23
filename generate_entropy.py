"""
    Iterate through all the questions and answers to generate a dict mapping term to its entropy value.
    Store the dict in entropies.pkl.
"""

import csv
from collections import defaultdict

class EntropyCalculator:
    def __init__(self):
        self.term2count = defaultdict(int)
        self.term2discussion2count = {}
        self.questions_fn = '../pythonquestions/Questions.csv'
        self.answers_fn = '../pythonquestions/Answers.csv'
        self.tags_fn = '../pythonquestions/Tags.csv'

    
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
                if count > 10:
                    break
                if questions:
                    question_id, _, _, _, _, body = line
                else:
                    _, _, _, question_id, _, body = line
                print question_id



    def count_terms(self):
        """Iterate through all discussions (questions & answers) to count the occurrences of terms.
        
        Update term2count and term2discussion2count.
        """
        self.process_csv()
        print ''
        self.process_csv(False)



def main():
    e = EntropyCalculator()
    e.count_terms()


if __name__ == '__main__':
    main()


