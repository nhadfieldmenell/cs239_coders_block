
# coding: utf-8

# In[3]:

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import *
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer


# In[6]:

'''
Iterate through the entire tags database, preprocess the content of the tags
and creare an Id -> set of tags dataframe to be used for scoring the tag similarity of the query.
'''
# Load data and use correct encoding 
#qdf = pd.read_csv('pythonquestions/Questions.csv', encoding='iso-8859-1')
tdf = pd.read_csv('pythonquestions/Tags.csv', encoding='iso-8859-1')
# Using nltk data for stop words etc'
nltk.data.path.append('/Users/orpaz/Developer/nltk_data')


# In[39]:

def stem_tags(data):
    for i, row in data.iterrows():
        if type(row['Tag']) is str:
            st = " ".join(re.findall("[a-zA-Z]+", row['Tag']))
            data.set_value(i, "Tag", st)


# In[ ]:

def aggregate_tags(data):
    data = data.groupby('Id').agg(lambda x: set(x))


# In[40]:

# The result of these step can be tested for the intersection with the tags from the query
if __name__ == '__main__':
    stem_tags(tdf)
    aggregate_tags(tdf)
    #df = qdf.join(tdf.set_index('Id'), on='Id')

