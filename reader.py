# This Python script will load text from a text file and create a vocabulary list
# by using a topic modling process like SVD, NMF or LDA. It then creates an html 
# table with the original sentences on one line and the parts of speech on the 
# following line. The purpose is to make reading a foreign language easier for
# a language student. Each word in the original sentence will be a link to a
# wordreference.com translation.

# There will also be two links for each sentence: one link that goes to google translate
# and one link that creates a sentence diagram.

# Imports from python
import re
from math import floor
import numpy as np

# Imports from SpaCy
import spacy
from spacy.lang.en.examples import sentences
from spacy.lang.es.stop_words import STOP_WORDS

# Imports froms Scikit-Learn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF, TruncatedSVD, LatentDirichletAllocation 
from sklearn.decomposition import TruncatedSVD as SVD 
from sklearn.decomposition import LatentDirichletAllocation as LDA

from readerlib import make_corpus, word_count

with open('news.txt', 'r') as f:
    text = f.read()

words = word_count(make_corpus(text))
print('Words:', words)
print('Topics:', floor(np.log2(words)))

cv = CountVectorizer(stop_words=STOP_WORDS, strip_accents=None)
word_vec = cv.fit_transform(make_corpus(text))
print(word_vec)

exit()

nlp = spacy.load('es_core_news_sm')
doc = nlp("Eso nos lleva a las elecciones del 20 de octubre del 2019 donde Evo buscaba un cuarto período presidencial")
print(doc.text)
for token in doc:
    print(token.text, token.pos_, token.lemma_)

