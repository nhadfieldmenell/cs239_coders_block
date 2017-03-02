
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import pickle


# In[145]:

def preprocess(questions, answers):
    for i, row in answers.iterrows():
        parent = row['ParentId']
        idx = dfq.loc[dfq['Id'] == parent].index[0]
        body = dfq.loc[dfq['Id'] == parent]['Body']
        body = (body + '\n' + row['Body']).astype(str)
        if i == 1:
            print(idx)
            print(body[idx])
        questions.set_value(idx, 'Body', body[idx])


# In[146]:

preprocess(dfq, dfa)


# In[ ]:

if __name__ == '__main__':
    dfq = pd.read_csv('pythonquestions/Questions.csv', encoding='iso-8859-1')
    dfa = pd.read_csv('pythonquestions/Answers.csv', encoding='iso-8859-1')
    dfq.to_csv('pythonquestions/Discussions.csv', encoding='iso-8859-1')

