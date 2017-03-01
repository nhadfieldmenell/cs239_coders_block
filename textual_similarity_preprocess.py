
# coding: utf-8

# In[82]:

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import *
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer


# In[52]:

'''
Iterate through the entire question database, preprocess the content of the 'Body'
and creare a Tf/Idf matrix to be used for scoring the query from the client.
'''

# Load data and use correct encoding
df = pd.read_csv('pythonquestions/Questions.csv', encoding='iso-8859-1')
# Using nltk data for stop words etc'
nltk.data.path.append('/Users/orpaz/Developer/nltk_data')


# In[61]:

def stem_data(data):
    '''
    Helper function to stem the body.
    '''
    stemmer = SnowballStemmer('english')

    for i, row in data.iterrows():
        q = (" ").join([z for z in BeautifulSoup(row['Body'], 'html5lib').get_text(" ").split(" ")])
        q = re.sub("[^a-zA-Z0-9]"," ", q)
        q = (" ").join([stemmer.stem(z) for z in q.split()])
        data.set_value(i, "processed_body", str(q))


# In[62]:

def remove_stop_words(data):
    '''
    Helper function to remove stop words
    from the body.
    '''
    stop = stopwords.words('english')

    for i, row in data.iterrows():
        q = row["processed_body"].lower().split(" ")
        q = (" ").join([z for z in q if z not in stop])
        data.set_value(i, "processed_body", q)


# In[143]:

def vectorizer(data):
    '''
    Fit a tf/idf model to be used for scoring queries against corpus.
    extract and save a dictionary of tokens and their idf score.
    save a transformed Tf-idf-weighted document-term matrix
    '''
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data['processed_body'])
    idf = vectorizer._tfidf.idf_
    tokens = dict(zip(vectorizer.get_feature_names(), idf))

    pickle.dump(vectorizer, open('tfidf_model.pkl', 'wb'))
    pickle.dump(X, open('questions_tfidf.pkl', 'wb'))
    pickle.dump(tokens, open('tokens_dict.pkl', 'wb'))


# In[ ]:


if __name__ == '__main__':
    stem_data(df)
    remove_stop_words(df)
    vectorizer(df)
