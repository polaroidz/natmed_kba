import nltk
import string
from nltk.corpus import stopwords

stop_words = stopwords.words('english')

# The low end of shared words to consider
LOWER_BOUND = .20

# The high end, since anything above this is probably SEO garbage or a
# duplicate sentence
UPPER_BOUND = .90

def is_unimportant(word):
    """Decides if a word is ok to toss out for the sentence comparisons"""
    return word in ['.', '!', ',', ] or '\'' in word or word in stop_words

def only_important(sent):
    """Just a little wrapper to filter on is_unimportant"""
    return filter(lambda w: not is_unimportant(w), sent)

def compare_sents(sent1, sent2):
    """Compare two word-tokenized sentences for shared words"""
    if not len(sent1) or not len(sent2):
        return 0
    
    return len(set(only_important(sent1)) & set(only_important(sent2))) / ((len(sent1) + len(sent2)) / 2.0)

def compare_sents_bounded(sent1, sent2):
    """If the result of compare_sents is not between LOWER_BOUND and
    UPPER_BOUND, it returns 0 instead, so outliers don't mess with the sum""" 
    cmpd = compare_sents(sent1, sent2)
    
    if LOWER_BOUND < cmpd < UPPER_BOUND:
        return cmpd
    else:
        return 0

def compute_score(sent, sents):
    """Computes the average score of sent vs the other sentences (the result of
    sent vs itself isn't counted because it's 1, and that's above
    UPPER_BOUND)"""
    if not len(sent):
        return 0
    
    return sum(compare_sents_bounded(sent, sent1) for sent1 in sents) / float(len(sents))

def summarize_block(block):
    """Return the sentence that best summarizes block"""
    if not block:
        return None
    
    sents = nltk.sent_tokenize(block)
    
    word_sents = list(map(nltk.word_tokenize, sents))
    
    d = dict((compute_score(word_sent, word_sents), sent)
             for sent, word_sent in zip(sents, word_sents))
    
    return d[max(d.keys())]

def tags_to_sent(tags):
    tags[0] = (tags[0][0].title(), tags[0][1])
    
    sent = " ".join([tag[0] for tag in tags])
    
    for p in string.punctuation:
        sent = sent.replace(" " + p, p)
    
    for p in ['(', '[', '{']:
        sent = sent.replace(p + " ", " " + p)
    
    return sent + '.'

def summarize(text):
    """Returns the sentence that summarizes the text corpus."""
    s_sent = summarize_block(text)
    s_tokens = nltk.word_tokenize(s_sent)
    s_tags = nltk.pos_tag(s_tokens)
    
    first_ok = False
    
    while not first_ok:
        if s_tags[0][1] in ['RB', '.', ',']:
            del s_tags[0]
        else:
            first_ok = True
    
    if s_tags[-1][1] in ['.', ',']:
        del s_tags[-1]
    
    compiled_sent = tags_to_sent(s_tags)
    
    return compiled_sent

def first_sentence(block):
    return nltk.sent_tokenize(block)[0]