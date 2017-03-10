
# coding: utf-8

# In[1]:

import textual_similarity
import tags_similarity
import API_methods_similarity


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

def question_scores():
    s = 0
    for i, row in df.iterrows():
        s += row['Score']


# In[6]:

txt_score = textual_similarity.tf_score(d)


# In[7]:

tgs_score = tags_similarity.tags_score(d)


# In[8]:

mth_score = API_methods_similarity.score_methods(d)


# In[30]:

mth_score = [float(i) for i in mth_score]


# In[31]:

tgs_score = [float(i) for i in tgs_score]


# In[33]:

txt_score = [float(i) for i in txt_score]


# In[38]:

txt_score = list(map(lambda x: x * 0.32, txt_score))
tgs_score = list(map(lambda x: x * 0.18, tgs_score))
mth_score = list(map(lambda x: x * 0.30, mth_score))


# In[42]:

res = [x + y + z for x, y, z in zip(txt_score, tgs_score, mth_score)]


# In[48]:

import numpy as np


# In[52]:

np.argsort(res)[-5:][::-1]


# In[56]:

textual_similarity.df.iloc[506700]['Body']


# In[ ]:



