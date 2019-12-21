from textblob import TextBlob
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from collections import Counter
import string
from summa import keywords


tokenizer = RegexTokenizer()
lemmatizer = WordNetLemmatizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)

# article functions
def sentiment(text, lang):
    if lang == 'english':
        blob = TextBlob(text)
        return blob.sentiment.polarity
    elif lang == 'russian':
        result = model.predict([text])[0]
        return result['positive'] - result['negative']

def meaningfullness(text, lang):
    tokens = [lemmatizer.lemmatize(i) for i in word_tokenize(text.lower(), language=lang) if i not in string.punctuation and len(i) > 2 and i not in stopwords.words(lang)]
    print(tokens)
    c = Counter(tokens)
    return len(c) / len(tokens)


def get_keywords(text):
    return keywords.keywords(text)


def get_bias(text, lang):
    return

# cluster functions
def top_title(cluster):
    return

def range_sentiment(cluster):
    return

def range_meaningfulness(cluster):
    return

def cluster_metrics(cluster):
    return {
        "date_range": publication_range,
        "ru_count": ru_count,
        "en_count": en_count,

    }

# corpus functions

def sentiment_top(corpus):
    return {
        "pos": pos_top,
        "neg": neg_top,
        "neu": neu_top
    }

def meaningfullness_top(corpus):
    return {
        "pos": pos_top,
        "neg": neg_top,
        "neu_top": neu_top
    }