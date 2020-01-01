import re
import spacy

nlp = spacy.load('es_core_news_sm')
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

def display_topics(model, feature_names, no_top_words, topic_names=None):
    """Prints the topics found my matrix decomposition."""
    for ix, topic in enumerate(model.components_):
        if not topic_names or not topic_names[ix]:
            print("\nTopic ", ix)
        else:
            print("\nTopic: '",topic_names[ix],"'")
        print(", ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))

def get_named_entities(text):
    """Uses spacy named entity recognition to identify enitites for each sentence in a
    corpus, and returns a list of lists of named entities."""
    entities = {}
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    doc = nlp(text)
    for ent in doc.ents:
        entities[ent.text] = ent.label_
    key_list = list(entities.keys())
    # Sapcy creates a lot of similar entities. The next two for loops will delete
    # any entitiy that is completly contained in another entitiy.
    keys_to_delete = set()
    for key in key_list:
        for other_key in key_list:
            if key != other_key and key in other_key:
                keys_to_delete.add(key)
    for key in keys_to_delete:
        del(entities[key])
    return entities

def get_parts_of_speech(corpus):
    """Returns the words in a sentence with their tagged parts of speech."""
    tagged_sentences = []
    for doc in corpus:
        doc_words = []
        tagged_doc = nlp(doc)
        for word in tagged_doc:
           doc_words.append((word.text, word.pos_))
        tagged_sentences.append(doc_words)
    return tagged_sentences


def add_word_reference_links(tagged_docs):
    """Takes a list of parts of speech tagged documents and converts the individuak
    words in each document to a link on the wordreference.com website."""
    link_base = 'https://www.wordreference.com/es/en/translation.asp?spen={}'
    linked_docs = []
    for doc in tagged_docs:
        word, pos = doc
        linked_docs.append((link_base.format(word), word, pos))
    return linked_docs
 


# Part of speech to description provides a more descriptive name to each part of
# speech (pos)
pos_to_desc = {
    'ADJ': 'adjective',
    'ADP': 'adposition',
    'ADV': 'adverb',
    'AUX': 'auxiliary verb',
    'CONJ': 'coordinating conjunction',
    'DET': 'determiner',
    'INTJ': 'interjection',
    'NOUN': 'noun',
    'NUM': 'numeral',
    'PART': 'particle',
    'PRON': 'pronoun',
    'PROPN': 'proper noun',
    'PUNCT': 'punctuation',
    'SCONJ': 'subordinating conjunction',
    'SYM': 'symbol',
    'VERB': 'verb'
}