from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

def tokenize(text):
    '''
    PARAMETERS:
    text (string) - raw text or sentence

    RETURN:
    clean_tokens (string[]) - cleaned tokens
    '''
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens