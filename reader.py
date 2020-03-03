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
from sklearn.decomposition import NMF 
from sklearn.decomposition import TruncatedSVD as SVD 
from sklearn.decomposition import LatentDirichletAllocation as LDA

# Local imports
from readerlib import *

# Read text file with the text to process.
with open('news.txt', 'r') as f:
    text = f.read()

nlp = spacy.load('es_core_news_sm')
# Create a corpus, count the words and set the number of topics
corpus = make_corpus(text)
# Determine language.
nlp, lang = determine_language(corpus, nlp)
print(lang)
words = word_count(corpus)
n_topics = floor(np.log2(words))
entities = get_named_entities(text, nlp)
entities_list = make_named_entity_list(entities)

# Create a the CountVectorizer and NMF objects.
cv = CountVectorizer(stop_words=STOP_WORDS, strip_accents=None)
word_vec = cv.fit_transform(make_corpus(text))
# nmf = NMF(n_components=n_topics, shuffle=True)
nmf = LDA(n_components=n_topics)
topics = nmf.fit_transform(word_vec)
vocabulary= create_vocab(nmf, cv.get_feature_names(), 5)
marked_sentences = get_parts_of_speech(corpus, nlp)
marked_sentences = add_word_reference_links(marked_sentences, lang)

with open('base.html', 'r') as f:
    base = f.read()

base = re.sub(r'<\$REPLACE\$>', make_tables(marked_sentences), base)
base = re.sub(r'<\$NAMED_ENTITIES\$>', entities_list, base)
base = re.sub(r'<\$VOCAB\$>', vocabulary, base)

with open('index.html', 'w') as fo:
    fo.write(base)

print(type(nlp))