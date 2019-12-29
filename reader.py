import re
from math import floor
import spacy
from spacy.lang.en.examples import sentences
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF, TruncatedSVD, LatentDirichletAllocation 
from sklearn.decomposition import TruncatedSVD as SVD 
from sklearn.decomposition import LatentDirichletAllocation as LDA

def make_corpus(raw_text):
    """Converts raw text into a corpus by splitting the text on end of sentences
    on end of line characters (.!?), and stripping non-word characters."""
    sentences = re.split(r'[\.\!\?]', raw_text)
    sentences = [re.sub(r'\W', ' ', sent) for sent in sentences]
    sentences = [re.sub(r'\s+', ' ', sent).strip() for sent in sentences]
    return sentences

def word_count(list_of_strings):
    """Returns a word count of a corpus."""
    counter = 0
    for string in list_of_strings:
        counter += len(re.findall(r' ', string)) + 1
    return counter

words = word_count(make_corpus(text))
print('Words:', words)
print('Topics:', floor(np.log2(words)))

exit()

nlp = spacy.load('es_core_news_sm')
doc = nlp("Eso nos lleva a las elecciones del 20 de octubre del 2019 donde Evo buscaba un cuarto período presidencial")
print(doc.text)
for token in doc:
    print(token.text, token.pos_, token.lemma_)

