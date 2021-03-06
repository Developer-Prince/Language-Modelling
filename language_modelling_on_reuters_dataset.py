# -*- coding: utf-8 -*-
"""Language_Modelling_on_Reuters_dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1M2TwVt2L3djNwgdKaq7YPlraqm-dprpf

# Language Modelling on Reuters Dataset

## 1. <font color='yellow'>Importing All Libraries </font>
"""

import numpy as np
import pandas as pd
import re
import random
from tqdm import tqdm
import spacy
import pickle
nlp = spacy.load('en_core_web_sm')

"""## 2. <font color = 'yellow'>Load Dataset </font>"""

# Loading Dataset
dialogs = pd.read_csv('/content/drive/MyDrive/Project - Next  Word Recommender System/sample_reuters_dataset.csv')

dialogs.head()

dialogs.shape

dialogs['sentence_text'][2]

"""## 3. <font color = 'yellow'>Text Preprocessing </font>"""

def preprocess(sentence):
    sentence = sentence.lower()
    sentence = re.sub("[-]",' ',sentence)
    sentence = re.sub("[^a-zA-Z' ]",'',sentence)
    sentence = re.sub('[\s ]+',' ',sentence)
    return sentence

preprocess(dialogs['sentence_text'][0])

preprocess(dialogs['sentence_text'][4])

dialogs_clean = []
for i in dialogs['sentence_text']:
    dialogs_clean.append(preprocess(i))

dialogs['clean_sentence'] = dialogs_clean

dialogs.head(10)

"""# Creating Unigrams"""

# Now we have the dataset then we have to only create the unigrams, bigrams and the trigrams first
# first we need to create the tokens for unigrams
def create_unigrams(sentence):
    tokens = sentence.split()
    unigrams_list = []
    for i in range(len(tokens)):
        unigrams_list.append(tokens[i:i+1])
    return unigrams_list

dialogs['unigrams'] = dialogs['clean_sentence'].apply(lambda x : create_unigrams(x))
dialogs.head()

"""# Creating Bigrams"""

def create_bigrams(sentence):
    tokens = sentence.split()
    bigrams_list = []
    for i in range(len(tokens)-1):
        bigrams_list.append(tokens[i:i+2])
    return bigrams_list

dialogs['bigrams'] = dialogs['clean_sentence'].apply(lambda x:create_bigrams(x))
dialogs.head(10)

"""# Creating Trigrams"""

def create_trigrams(sentence):
    tokens = sentence.split()
    trigrams_list = []
    for i in range(len(tokens)-2):
        trigrams_list.append(tokens[i:i+3])
    return trigrams_list

dialogs["trigrams"] = dialogs['clean_sentence'].apply(lambda x: create_trigrams(x))
dialogs.head(3)

"""# Building Language Model"""

from collections import Counter  , defaultdict

# creating placeholder for model
model = defaultdict(lambda: defaultdict(lambda:  0))

for i in range(dialogs.shape[0]):
    for w1,w2,w3 in create_trigrams(dialogs['clean_sentence'][i]):
    #counts the occurence of w3 when w1 and w2 is given
        model[(w1,w2)][w3] += 1

model

"""# Predicting Next Word Based on Previous Two Words"""

# Predicting the next word
dict(model['i','am'])

# Creating the Unigram Dict
unigram_dict = {}
for i in tqdm(range(dialogs.shape[0])):
    for word in dialogs['unigrams'][i]:
        if word[0] in unigram_dict:
            unigram_dict[word[0]] += 1
        else:
            unigram_dict[word[0]] = 1

dialogs.head()

unigram_dict

total_length = len(unigram_dict)
counts = Counter(unigram_dict)

for word in counts:
    counts[word] = counts[word]/total_length

counts

for w1_w2 in model:
    total_counts = float(sum(model[w1_w2].values()))
    for w3 in model[w1_w2]:
        model[w1_w2][w3] /= total_length

max(dict(model['they','told']))

