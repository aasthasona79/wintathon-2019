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


# In[2]:


## READ CSVs
dfUsers = pd.read_csv('Users.csv')
dfEvents = pd.read_csv('Events.csv')


# In[3]:


## Remove stop words in english
def removeStopwords(sentence):
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(sentence)   
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    filtered_sentence = [] 
    for w in word_tokens: 
        if w not in stop_words: 
            filtered_sentence.append(w) 
    return ' '.join(filtered_sentence)


# In[4]:


## Remove punctuations
def removePunctuations(sentence):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    no_punct = ""
    for char in sentence:
        if char not in punctuations:
            no_punct = no_punct + char
    return no_punct


# In[5]:


## Extract company name tags present in the profile
def extractCompanyTags(para):
    df_Company_csv = pd.read_csv('Companies.csv')
    df_Companies = pd.DataFrame(columns = ['Company'])
    df_Companies['Company'] = df_Company_csv['Company']
    df_Companies['Company'] = df_Companies['Company'].astype(str).str.lower()
    filteredTags = []
    for index,row in df_Companies.iterrows():
        if row['Company'].lower() in para.lower():
            filteredTags.append(row['Company'].lower())
    return filteredTags


# In[6]:


## Extract tech keywords tags present 
def extractKeywords(para):
    df_keywords_csv = pd.read_csv('Tech words.csv')
    df_keywords_csv['Keys'] = df_keywords_csv['Keys'].astype(str).str.lower()
    filteredTags = []
    for index,row in df_keywords_csv.iterrows():
        if row['Keys'] in para.lower():
            filteredTags.append(row['Keys'])
    return filteredTags


# In[7]:


## Extract and compile tags in User csv
def UserCleaning(dfUsers):
    filtered_sentences = []
    for i in range(len(dfUsers.index)):
        sent = dfUsers.loc[i]['Jobs Applied']
        list3 = []
        if(type(sent)!=str):
            list3 = list3
        else:
            sent = sent.lower()
            sent = removeStopwords(sent)
            sent = removePunctuations(sent)
            list1 = extractCompanyTags(sent)
            list2 = extractKeywords(sent)
            list3 = list1 + list2
        sent = dfUsers.loc[i]['Job Experience']
        if(type(sent)!=str):
            list3 = list3
        else:
            sent = sent.lower()
            sent = removeStopwords(sent)
            sent = removePunctuations(sent)
            list1 = extractCompanyTags(sent)
            list2 = extractKeywords(sent)
            list3 = list3 + list1 + list2
        list3 = list3 + extractKeywords(dfUsers.loc[i]['Skills'])
        filtered_sentences.append(list3)
    dfUsers['Tags'] = filtered_sentences
    return dfUsers


# In[8]:


## Extract and compile all tags from events csv
def EventCleaning(dfEvents):
    filtered_sentences = []
    for i in range(len(dfEvents.index)):
        sent = dfEvents.loc[i]['Description']
        if(type(sent)!=str):
            list3 = []
        else:
            sent = sent.lower()
            sent = removeStopwords(sent)
            sent = removePunctuations(sent)
            list1 = extractCompanyTags(sent)
            list2 = extractKeywords(sent)
            list3 = list1 + list2
        list3 = list3 + extractKeywords(dfEvents.loc[i]['Skills'])
        filtered_sentences.append(list3)
    dfEvents['Tags'] = filtered_sentences
    return dfEvents


# In[9]:


dfUsers = UserCleaning(dfUsers)


# In[10]:


dfEvents = EventCleaning(dfEvents)


# In[11]:


## Extracts user tags given user name
def userTags(user,dfUsers):
    listUserTags = list()
    for index,row in dfUsers.iterrows():
        if row['User Name'] == user:
            return list(set(row['Tags']))

## Calculates similarity score
def calculateScore(userTags,df):
    scores = []
    for index,row in df.iterrows():
        eventTags = list(set(row['Tags']))
        common = retCommon(eventTags, userTags)
        scores.append(len(common)/(len(userTags)))
    sv = pd.Series(scores)
    df['scores'] = sv.values
    return df

## Returns common tags between two lists
def retCommon(list1,list2):
    common = []
    for ele in list2:
        if ele in list1:
            common.append(ele)
    common = list(set(common))
    return common

dfEvents = calculateScore(userTags('Alex',dfUsers),dfEvents)
dfEvents.to_csv('Updated Events.csv')

