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
    keys_to_delete = set()
    for key in key_list:
        for other_key in key_list:
            if key != other_key and key in other_key:
                keys_to_delete.add(key)
    # print(entities.keys())
    print(keys_to_delete)
    for key in keys_to_delete:
        del(entities[key])
    return entities


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