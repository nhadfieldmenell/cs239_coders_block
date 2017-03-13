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
import random


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
        reputation = -1
    return reputation

def gen_uids_reps():
    with open('uids_questions.pkl', 'rb') as infile:
        uids = pickle.load(infile)

    uids = [i for i in uids]
    random.shuffle(uids)
    uids_reps = [uids, []]
    with open('uids_reps.pkl', 'wb') as outfile:
        pickle.dump(uids_reps, outfile)

def update_avg_reputation():
    uid_rep_fn = 'uids_reps.pkl'
    with open(uid_rep_fn, 'rb') as infile:
        uids_reps = pickle.load(infile)

    reps = uids_reps[1]
    if reps:
        avg_rep = sum(reps) / len(reps)
        print 'AVERAGE REPUTATION BEFORE'
        print avg_rep
    while True:
        uid = uids_reps[0].pop()
        rep = extract_reputation(uid)
        print rep
        if rep == -1:
            break
        uids_reps[1].append(rep)

    with open(uid_rep_fn, 'wb') as outfile:
        pickle.dump(uids_reps, outfile)

    reps = uids_reps[1]
    avg_rep = float(sum(reps)) / float(len(reps))
    print 'AVERAGE REPUTATION AFTER'
    print avg_rep
    with open('reputation_question_avg.pkl', 'wb') as outfile:
        pickle.dump(avg_rep, outfile)
        

def average_reputation(num_to_avg=120, in_fn='uids_questions.pkl'):
    """Calculate the average repuation of question askers in the data dump.
    """
    with open(in_fn, 'rb') as infile:
        uids = pickle.load(infile)

    uids = [i for i in uids]
    choices = random.sample(xrange(len(uids)), num_to_avg)
    selected_uids = [uids[i] for i in choices]

    reps = []
    for uid in selected_uids:
        rep = extract_reputation(uid)
        print rep
        if rep >= 0:
            reps.append(float(rep))
    avg_rep = sum(reps) / len(reps)
    print 'AVERAGE REPUTATION'
    print avg_rep

    with open('reputation_question_avg.pkl', 'wb') as outfile:
        pickle.dump(avg_rep, outfile)


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
    update_avg_reputation()
    return
    average_reputation()
    r = ReputationCalculator()
    r.parse_uids()
    r.register_reputations()

if __name__ == '__main__':
    main()
