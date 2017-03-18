
# coding: utf-8

# In[1]:

import textual_similarity
import tags_similarity
import API_methods_similarity
from datetime import datetime
import numpy as np
import pickle
import math


# In[2]:

## An example query containing quicksort algorithm
d = {'imports' : {'pandas', 'numpy', 'scipy'}, 
     'methods' : ['quickSort', 'quickSortHelper', 'partition'], 
     'code' : '''function quicksort(array)
    if length(array) > 1
        pivot := select any element of array
        left := first index of array
        right := last index of array
        while left ≤ right
            while array[left] < pivot
                left := left + 1
            while array[right] > pivot
                right := right - 1
            if left ≤ right
                swap array[left] with array[right]
                left := left + 1
                right := right - 1
        quicksort(array from first index to right)
        quicksort(array from left to last index)'''}


# In[3]:

def sigmoid(x ,avg):
    return 1 / (1 + math.exp(avg-x))


# In[4]:

def get_scores(d):
    # Time the function
    startTime = datetime.now()
    txt_score = textual_similarity.tf_score(d)
    print ("Textual finished after: " + str(datetime.now() - startTime))
    startTime = datetime.now()
    tgs_score = tags_similarity.tags_score(d)
    print ("Tags finished after: " + str(datetime.now() - startTime))
    startTime = datetime.now()
    mth_score = API_methods_similarity.score_methods(d)
    print ("Methods finished after: " + str(datetime.now() - startTime))
    qtn_score = textual_similarity.df.Score
    
    startTime = datetime.now()
    mth_score = [float(i) for i in mth_score]
    tgs_score = [float(i) for i in tgs_score]
    txt_score = [float(i) for i in txt_score]
    avg = np.mean(qtn_score)
    qtn_score = [sigmoid(i, avg) for i in qtn_score]
    
    txt_score = list(map(lambda x: x * 0.32, txt_score))
    tgs_score = list(map(lambda x: x * 0.18, tgs_score))
    mth_score = list(map(lambda x: x * 0.30, mth_score))
    qtn_score = list(map(lambda x: x * 0.07, qtn_score))
    
    res = [x + y + z + w for x, y, z, w in zip(txt_score, tgs_score, mth_score, qtn_score)]
    
    #top 5
    top = np.argsort(res)[-5:][::-1]
    
    print ("All the rest finished after: " + str(datetime.now() - startTime))
    
    return top


# In[6]:

if __name__ == '__main__':
    with open('code_context.pkl', 'rb') as f:
        q = pickle.load(f)
    top = get_scores(q)


# In[8]:

top


# In[ ]:

textual_similarity.df.iloc[224237]['Id']


# In[ ]:



