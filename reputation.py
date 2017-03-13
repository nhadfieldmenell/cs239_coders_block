"""Script containing method to extract a user's reputation (extract_reputation).
"""


from lxml import html
import pickle
import requests
import re
import time
from collections import defaultdict
import csv
import pdb


def extract_reputation(uid):
    """Lookup a user's reputation.

    Args:
        uid: StackOverflow user id.

    Return:
        That user's reputation.
    """

    page = requests.get('http://stackoverflow.com/users/%d' % uid)
    tree = html.fromstring(page.content)
    try:
        reputation = int(re.sub(',', '', tree.xpath('//div[@title="reputation"]/text()')[0].strip()))
    except:
        print "PROBLEM EXTRACTING REPUTATION"
        reputation = 0
    return reputation





class ReputationCalculator:
    def __init__(self):
        self.questions_fn = '../pythonquestions/Questions.csv'
        self.answers_fn = '../pythonquestions/Answers.csv'
        self.uids = set()
        self.uid2reputation = defaultdict(int)

    def parse_uids(self):
        """Extract all uids.
        """
        self.process_csv(True)
        """
        print 'processed questions'
        self.process_csv(False)
        """
        print len(self.uids)
        with open('uids_questions.pkl', 'wb') as outfile:
            pickle.dump(self.uids, outfile)


    def process_csv(self, questions=True):
        """Extract uids from the Questions/Answers file.

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
                if count % 100000 == 0:
                    print count
                    print 'time to process 100000: %.2f' % (time.time()-cur_time)
                    cur_time = time.time()
                _, uid, _, _, _, _ = line
                if uid != 'NA':
                    self.uids.add(int(uid))
        print 'read %d lines' % count


    def register_reputations(self):
        counter = 0
        cur_time = time.time()
        for uid in self.uids:
            counter += 1
            if counter % (len(self.uids) / 10) == 0:
                print 'chunk %d in %.2fs' % (counter / (len(self.uids) / 10), time.time() - cur_time)
                cur_time = time.time()
            self.uid2reputation[uid] = extract_reputation(uid)

        with open('uid2reputation.pkl', 'wb') as outfile:
            pickle.dump(self.uid2reputation, outfile)



def main():
    r = ReputationCalculator()
    r.parse_uids()
    return
    r.register_reputations()

if __name__ == '__main__':
    main()
