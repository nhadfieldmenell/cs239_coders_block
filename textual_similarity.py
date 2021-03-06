
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
from sklearn.metrics.pairwise import linear_kernel


# In[2]:

'''
Iterate through the entire question database, preprocess the content of the 'Body'
and creare a Tf/Idf matrix to be used for scoring the query from the client.
'''

df = pd.read_csv('pythonquestions/Discussions.csv', encoding='iso-8859-1')
nltk.data.path.append('/Users/orpaz/Developer/nltk_data')
disc = pickle.load(open('tex_sim_pkls/questions_tfidf.pkl', 'rb'))


# In[12]:

def stem_data(data, query = False):
    '''
    Helper function to stem the body. 
    Remove code componenet from the data, use a snowball stemmer to stem the data.
    Add a column for the processed text
    '''
    stemmer = SnowballStemmer('english')
    
    if not query:
        for i, row in data.iterrows():
            soup = BeautifulSoup(row['Body'], 'html5lib')
            codetags = soup.find_all('code')
            for codetag in codetags:
                codetag.extract()
            q = (" ").join([z for z in soup.get_text(" ").split(" ")])
            q = re.sub("[^a-zA-Z0-9]"," ", q)
            q = (" ").join([stemmer.stem(z) for z in q.split()])
            data.set_value(i, "processed_body", str(q))
    else:
        soup = BeautifulSoup(data['code'], 'html5lib')
        codetags = soup.find_all('code')
        for codetag in codetags:
            codetag.extract()
        q = (" ").join([z for z in soup.get_text(" ").split(" ")])
        q = re.sub("[^a-zA-Z0-9]"," ", q)
        q = (" ").join([stemmer.stem(z) for z in q.split()])
        return q


# In[17]:
def remove_stop_words(data, query = False):
    '''
    Helper function to remove stop words
    from the body using nltk english defined stop words.
    '''
    stop = stopwords.words('english')
    
    if not query:
        for i, row in data.iterrows():
            q = row["processed_body"].lower().split(" ")
            q = (" ").join([z for z in q if z not in stop])
            data.set_value(i, "processed_body", q)
    else:
        q = data['code'].lower().split(" ")
        q = (" ").join([z for z in q if z not in stop])
        return q


# In[42]:

def vectorizer(data, save = False, query = False):
    '''
    Fit a tf/idf model to be used for scoring queries against corpus.
    extract and save a dictionary of tokens and their idf score.
    save a transformed Tf-idf-weighted document-term matrix
    '''
    if not query:
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(data['processed_body'])
        idf = vectorizer._tfidf.idf_
        tokens = dict(zip(vectorizer.get_feature_names(), idf))
    else:
        mdl = pickle.load(open('tex_sim_pkls/tfidf_model.pkl', 'rb'))
        X = mdl.transform([data['code']])
        return X
    
    if save:
        pickle.dump(vectorizer, open('tex_sim_pkls/tfidf_model.pkl', 'wb')) 
        pickle.dump(X, open('tex_sim_pkls/questions_tfidf.pkl', 'wb')) 
        pickle.dump(tokens, open('tex_sim_pkls/tokens_dict.pkl', 'wb'))
    
    return X


# In[2]:

def cosine_sim(query, base):
    '''
    Calculate the cosine similarity of query vs the base TF/IDF model
    '''
    cosine_similarities = linear_kernel(query, base).flatten()
    ## Get indices of top 5 docs that maximize tfidf cosine
    related_docs_indices = cosine_similarities.argsort()[:-7:-1]
    print("Indices of best docs: " + str(related_docs_indices))
    print("Best docs cosine score: " + str(cosine_similarities[related_docs_indices]))
    return cosine_similarities


# In[87]:

def tf_score(d):
    '''
    Run the scoring function.
    '''
    d['code'] = stem_data(d, query = True)
    d['code'] = remove_stop_words(d, query = True)
    X = vectorizer(d, query = True)
    return cosine_sim(X,disc)


# In[48]:

if __name__ == '__main__': 
    # Using nltk data for stop words etc'
    stem_data(df)
    remove_stop_words(df)
    vectorizer(df)
    df.to_csv('pythonquestions/processed_discussions.csv', encoding='iso-8859-1', index=False)

