
# coding: utf-8

# In[9]:

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import *
import re
import pickle
from collections import deque
from ast import literal_eval


# In[10]:

'''
Iterate through the entire tags database, extract the code component of the discussion, 
snowball stemming the extracted code and removing non alphabetical charecters.
'''

data = pd.read_csv('pythonquestions/processed_discussions.csv', encoding='iso-8859-1')
df = [literal_eval(x) for x in data['Methods'].fillna("[]")]


# In[11]:

def stem_data(data):
    '''
    Helper function to stem the body.
    '''
    stemmer = SnowballStemmer('english')

    for i, row in data.iterrows():
        q = [z.get_text(" ").split(" ") for z in BeautifulSoup(row['Body'], 'html5lib').findAll('code')]
        if q:  
            q = (" ").join([item for sublist in q for item in sublist])
            q = re.sub("[^a-zA-Z0-9]"," ", q)
            q = [stemmer.stem(z) for z in q.split()]
            data.set_value(i, "Methods", str(q))


# In[29]:

def score_methods(d):
'''
Scoring function for comparing the methods used in the clients query
to the methods mentiond in the stackoverflow discussions.
'''
    lst = list()
    for row in df:
        if type(row) is str:
            s = set(row) & set(d['methods'])
            res = len(s) / len(set(d['methods']))
            lst.append(res)
        else:
            lst.append(0)
    return lst


# In[10]:

if __name__ == '__main__':
    # n = data.sample(n=20)
    stem_data(data)
    data.to_csv('pythonquestions/processed_discussions.csv', encoding='iso-8859-1', index=False)


# In[26]:



