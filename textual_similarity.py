
# coding: utf-8

# In[42]:

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import *
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


# In[43]:

'''
Iterate through the entire question database, preprocess the content of the 'Body'
and creare a Tf/Idf matrix to be used for scoring the query from the client.
'''


# In[44]:

def stem_data(data):
    '''
    Helper function to stem the body.
    '''
    stemmer = SnowballStemmer('english')

    for i, row in data.iterrows():
        soup = BeautifulSoup(row['Body'], 'html5lib')
        codetags = soup.find_all('code')
        for codetag in codetags:
            codetag.extract()
        q = (" ").join([z for z in soup.get_text(" ").split(" ")])
        q = re.sub("[^a-zA-Z0-9]"," ", q)
        q = (" ").join([stemmer.stem(z) for z in q.split()])
        data.set_value(i, "processed_body", str(q))


# In[45]:

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


# In[46]:

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
    
    pickle.dump(vectorizer, open('tex_sim_pkls/tfidf_model.pkl', 'wb')) 
    pickle.dump(X, open('tex_sim_pkls/questions_tfidf.pkl', 'wb')) 
    pickle.dump(tokens, open('tex_sim_pkls/tokens_dict.pkl', 'wb')) 


# In[47]:

def cosine_sim(query, base):
    cosine_similarities = linear_kernel(query, base).flatten()
    ## Get indices of top 5 docs that maximize tfidf cosine
    related_docs_indices = cosine_similarities.argsort()[:-7:-1]
    print("Indices of best docs: " + str(related_docs_indices))
    print("Best docs cosine score: " + str(cosine_similarities[related_docs_indices]))
    return related_docs_indices


# In[ ]:

if __name__ == '__main__':
    # Load data and use correct encoding 
    df = pd.read_csv('pythonquestions/Discussions.csv', encoding='iso-8859-1')
    # Using nltk data for stop words etc'
    nltk.data.path.append('/Users/orpaz/Developer/nltk_data')
    stem_data(df)
    remove_stop_words(df)
    vectorizer(df)
    df.to_csv('pythonquestions/processed_discussions.csv', encoding='iso-8859-1')


# In[ ]:

## In order to score the query use the following steps after query tfidf preprocess
x = pickle.load(open('tex_sim_pkls/questions_tfidf.pkl', 'rb'))
a = x[0:1]
cosine_sim(a,x)


# In[ ]:



