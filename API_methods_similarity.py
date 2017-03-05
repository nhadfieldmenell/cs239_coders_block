
# coding: utf-8

# In[50]:

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import *
import re
import pickle
import ast
from collections import deque


# In[200]:

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


# In[ ]:

if __name__ == '__main__':
    data = pd.read_csv('pythonquestions/Questions.csv', encoding='iso-8859-1')
    # n = data.sample(n=20)
    stem_data(data)


# In[ ]:



