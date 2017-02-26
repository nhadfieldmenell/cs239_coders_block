
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

# Load data and use correct encoding 
qdf = pd.read_csv('pythonquestions/Questions.csv', encoding='iso-8859-1')
tdf = pd.read_csv('pythonquestions/Tags.csv', encoding='iso-8859-1')
# Using nltk data for stop words etc'
nltk.data.path.append('/Users/orpaz/Developer/nltk_data')


# In[8]:

qdf.join(tdf.set_index('Id'), on='Id')


# In[ ]:



