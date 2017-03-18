
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import *
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer


# In[3]:

'''
Iterate through the entire tags database, preprocess the content of the tags
and creare an Id -> set of tags dataframe to be used for scoring the tag similarity of the query.
'''

df = pd.read_csv('pythonquestions/processed_discussions.csv', encoding='iso-8859-1')


# In[78]:

def stem_tags(data):
    for i, row in data.iterrows():
        if type(row['Tag']) is str:
            st = " ".join(re.findall("[a-zA-Z]+", row['Tag']))
            data.set_value(i, "Tag", st)


# In[79]:

def aggregate_tags(data):
    return (data.groupby('Id').agg(lambda x: set(x))).reset_index()


# In[56]:

def tags_score(d):
    lst = list()
    for i, row in df.iterrows():
        try:
            if row['Tag']:
                #print(row['Tag'], i)
                if 'nan,' in row['Tag'] or 'nan}' in row['Tag']:
                    s = eval(row['Tag'].replace('nan', "''")) & d['imports']
                else:
                    s = eval(row['Tag']) & d['imports']
                res = len(s) / len(row['Tag'])
                lst.append(res)
            else:
                lst.append(0)
        except:
            print(row['Tag'], i)
    return lst


# In[74]:

# The result of these step can be tested for the intersection with the tags from the query
if __name__ == '__main__':
    # Load data and use correct encoding
    qdf = pd.read_csv('pythonquestions/processed_discussions.csv', encoding='iso-8859-1')
    tdf = pd.read_csv('pythonquestions/Tags.csv', encoding='iso-8859-1')
    # Using nltk data for stop words etc'
    nltk.data.path.append('/Users/orpaz/Developer/nltk_data')
    stem_tags(tdf)
    tdf = aggregate_tags(tdf)
    #df = qdf.join(tdf.set_index('Id'), on='Id')
