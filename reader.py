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

# Local imports
from readerlib import make_corpus, word_count, display_topics, get_named_entities, get_parts_of_speech

# Read text file with the text to process.
with open('news.txt', 'r') as f:
    text = f.read()

# Create a corpus, count the words and set the number of topics
corpus = make_corpus(text)
words = word_count(corpus)
n_topics = floor(np.log2(words))
entities = get_named_entities(text)

# Create a the CountVectorizer and NMF objects.
cv = CountVectorizer(stop_words=STOP_WORDS, strip_accents=None)
word_vec = cv.fit_transform(make_corpus(text))
nmf = NMF(n_components=n_topics, shuffle=True)
topics = nmf.fit_transform(word_vec)
# display_topics(nmf, cv.get_feature_names(), 5)
marked_sentences = get_parts_of_speech(corpus)
for ms in marked_sentences:
    print(ms)

exit()

nlp = spacy.load('es_core_news_sm')
doc = nlp("Eso nos lleva a las elecciones del 20 de octubre del 2019 donde Evo buscaba un cuarto período presidencial")
print(doc.text)
for token in doc:
    print(token.text, token.pos_, token.lemma_)

