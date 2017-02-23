"""
    Iterate through all the questions and answers to generate a dict mapping term to its entropy value.
    Store the dict in entropies.pkl.
"""

from collections import defaultdict

class EntropyCalculator:
    def __init__(self):
        self.term2count = defaultdict(int)
        self.term2discussion2count = {}
        self.questions_fn = '../pythonquestions/Questions.csv'
        self.answers_fn = '../pythonquestions/Answers.csv'
        self.tags_fn = '../pythonquestions/Tags.csv'

    def count_terms(self):
        """Iterate through all discussions (questions & answers) to count the occurrences of terms.
        
        Update term2count and term2discussion2count.
        """
        pass



def main():
    e = EntropyCalculator()
    e.count_terms()


if __name__ == '__main__':
    main()


