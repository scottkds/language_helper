import re
import spacy
from spacy_readability import Readability
from spacy_langdetect import LanguageDetector
import pdb

MAX_TABLE_LENGTH = 10

nlp = spacy.load('es_core_news_sm')

# Part of speech to description provides a more descriptive name to each part of
# speech (pos)
pos_to_desc = {
    'ADJ': 'adjective',
    # 'ADP': 'adposition',
    'ADP': 'preposition',
    'ADV': 'adverb',
    'AUX': 'aux verb',
    'CONJ': 'coor-conj',
    'DET': 'determiner',
    'INTJ': 'interjection',
    'NOUN': 'noun',
    'NUM': 'numeral',
    'PART': 'particle',
    'PRON': 'pronoun',
    'PROPN': 'proper noun',
    'PUNCT': 'punctuation',
    'SCONJ': 'sub-conj',
    'SYM': 'symbol',
    'VERB': 'verb',
    'END': 'end'
}

def make_corpus(raw_text):
    """Converts raw text into a corpus by splitting the text on end of sentences
    on end of line characters (.!?), and stripping non-word characters."""
    sentences = re.split(r'\. |\.\n|\! |\!\n|\? |\?\n', raw_text)
    sentences = [re.sub(r'\W | \(' , ' ', sent) for sent in sentences]
    sentences = [re.sub(r'\s+', ' ', sent).strip() for sent in sentences]
    if sentences[-1] == '':
        sentences.pop(-1)
    return sentences

def word_count(list_of_strings):
    """Returns a word count of a corpus."""
    counter = 0
    for string in list_of_strings:
        counter += len(re.findall(r' ', string)) + 1
    return counter


def create_vocab(model, feature_names, no_top_words):
    """Creates a set of vocabulary words from a word count vectorizer decomposition."""
    vocab = set()
    for idx, topic in enumerate(model.components_):
        topic_words = [feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]
        for word in topic_words:
            vocab.add(word)
    return ', '.join(['<a href="https://www.wordreference.com/es/en/translation.asp?spen={}">{}</a>'.format(word, word) for word in vocab])

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
    # Spacy creates a lot of similar entities. The next two for loops will delete
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
#    import pdb; pdb.set_trace()
    """Returns the words in a sentence with their tagged parts of speech."""
    tagged_sentences = []
    for doc in corpus:
        doc_words = []
        tagged_doc = nlp(doc)
        for word in tagged_doc:
           doc_words.append((word.text, word.pos_))
        doc_words.append(('\u25E6', 'END'))
        tagged_sentences.append(doc_words)
    return tagged_sentences


def add_word_reference_links(tagged_docs):
    """Takes a list of parts of speech tagged documents and converts the individual
    words in each document to a link on the wordreference.com website."""
    link_base = 'https://www.wordreference.com/es/en/translation.asp?spen={}'
    google_base = 'https://translate.google.com/#view=home&op=translate&sl=es&tl=en&text='
    linked_docs = []
    google_tx = ''
    for doc in tagged_docs:
        linked_sent = []
        for tup in doc:
            word, pos = tup
            if word !=  '\u25E6':
                linked_sent.append((link_base.format(word), word, pos))
                google_tx += (word + '%20')
            else:
                linked_sent.append((google_base + google_tx, word, pos))
        linked_docs.append(linked_sent)
    return linked_docs

def make_cells(data):
    """Creates two CSS table cells from the input data. The data should be a tuple
    of three parts, a link, a word, and a part of speech. The result will be a 
    tuple of two cells. One for a word-link that will form part of the readable
    sentence, and a cell for the part of speech."""
    link, word, pos = data
    word_cell = """<div class="Cell"><a href="{}">{}</a></div>""".format(link, word)
    pos_cell = """<div class="Cell"><p>{}</p></div>""".format(pos)
    return (word_cell, pos_cell)

def make_word_cells(data):
    """Creates a CSS table cell from the input data. The data should be a tuple
    of three parts, a link, a word, and a part of speech. The result will be a 
    a a table cell with a word-link that will form part of the readable sentence."""
    link, word, pos = data
    word_cell = """<div class="Cell"><a href="{}">{}</a></div>""".format(link, word)
    return word_cell

def make_pos_cells(data):
    """Creates a CSS table cell from the input data. The data should be a tuple
    of three parts, a link, a word, and a part of speech. The result will be a 
    a a table cell with a part of speech."""
    link, word, pos = data
    # pos_cell = """<div class="Cell"><p>{}</p></div>""".format(pos_to_desc[pos])
    pos_cell = """<div class="Cell">{}</div>""".format(pos_to_desc[pos])
    return pos_cell
 
def make_row(tagged_sentence):
    """Creates a row for a table by mapping either make_word_cells or make_pos_cells
    to a tagged sentence."""
    rows = ''
    while tagged_sentence:
        sentence_part = tagged_sentence[:MAX_TABLE_LENGTH]
        rows += '<div class="Row">' + ''.join(map(make_word_cells, sentence_part)) + '</div>'
        rows += '<div class="Row">' + ''.join(map(make_pos_cells, sentence_part)) + '</div>'
        tagged_sentence = tagged_sentence[MAX_TABLE_LENGTH:]
    rows += make_empty_row()
    return rows

def make_empty_row():
    """Creates a row for a table by mapping either make_word_cells or make_pos_cells
    to a tagged sentence."""
    cells = ''
    # for num in range(MAX_TABLE_LENGTH):
    #     cells += '<div class="Cell"><p>___</p></div>'
    return '<div class="Row">' + cells + '</div>'

def make_tables(corpus):
    table_header = '<div class="Table">'
    table_footer = '</div>'
    table_content = ''
    # for doc in corpus:
    #     table_content += make_row(doc)
    # return table_header + table_content + table_footer
    for doc in corpus:
        table_content += table_header + make_row(doc) + table_footer + '<br><br>'
    return table_content 

def make_named_entity_list(entities):
    entities_html_list = ''
    for key in entities.keys():
        entities_html_list += ('<li>' + key + '</li>\n')
    return '<ul>\n' + entities_html_list + '</ul>\n'