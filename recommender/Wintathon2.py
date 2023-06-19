#!/usr/bin/env python
# coding: utf-8

# In[1]:


## Libraries
import numpy as np  
import pandas as pd
import matplotlib.pyplot as plt
import string
import math
import seaborn as sns
import nltk
from nltk.corpus import stopwords
import warnings
from nltk.stem import WordNetLemmatizer  
from nltk.tokenize import word_tokenize 
warnings.simplefilter("ignore", category=PendingDeprecationWarning)


# In[5]:


## READ CSVs
dfUsers = pd.read_csv('Users.csv')
dfEvents = pd.read_csv('Events.csv')
dfCons = pd.read_csv('Connections friends .csv')


# In[3]:


# Find user ID for a given user
def findUserID(user):
    for index,row in dfUsers.iterrows():
        if row['User Name'] == user:
            return row['User ID']


# In[7]:


# Find connections of a user
def findCon(userid):
    cons= []
    for index,row in dfCons.iterrows():
        if row['User ID'] == userid:
            cons.append(row['Con'])
    return cons


# In[11]:


# Find events that have user's connections as speakers
def findEvents(cons):
    events = []
    for index,row in dfEvents.iterrows():
        userid = findUserID(row['Speakers'])
        if userid in cons:
            events.append(1)
        else:
            events.append(0)
    sv = pd.Series(events)
    dfEvents['Recommend Connection'] = sv.values
    dfEvents.to_csv('Updated Events for speakers.csv')


# In[12]:


# Calling functions
userid = findUserID('Alex')
cons = findCon(userid)
findEvents(cons)

