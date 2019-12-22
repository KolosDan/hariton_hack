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
# article_obj: {"article": article, "lang": lang}
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
    if lang == 'english':
        return 1 - TextBlob(text).sentiment.subjectivity
    elif lang == 'russian':
        return model.predict([text])[0]['neutral']

def get_article_stats(article_obj):
    lang = article_obj['lang']
    article = article_obj['article']

    return {
        "sentiment": sentiment(article['text'], lang),
        "meaningfullness": meaningfullness(article['text'], lang),
        "bias": get_bias(article["text"], lang),
        "keywords": get_keywords(article['text'])
    }

# cluster functions
# cluster_obj: [article_obj_with_stats, ...]

# meaningfull_ness -> 1
# bias -> 1
def get_pravda(cluster_obj):
    return {'ru': max([i for i in cluster_obj if i['lang'] == 'ru'], key=lambda x: x['stats']['bias'] + x['stats']['meaningfullness'])['_id'],
    'en': max([i for i in cluster_obj if i['lang'] == 'en'], key=lambda x: x['stats']['bias'] + x['stats']['meaningfullness'])['_id']}

def range_sentiment(cluster_obj):
    ru = [i for i in cluster_obj if i['lang'] == 'ru']
    en = [i for i in cluster_obj if i['lang'] == 'en']

    ranged_ru = sorted(ru, key=lambda x: x['stats']['sentiment'])
    ranged_en = sorted(en, key=lambda x: x['stats']['sentiment'])

    return {
        'ru': {
            "low": [i['_id'] for i in ranged_ru[:5]],
            "high": [i['_id'] for i in ranged_ru[-5:]]
    }
    ,
        'en': {
            "low": [i['_id'] for i in ranged_en[:5]],
            "high": [i['_id'] for i in ranged_en[-5:]]
    }
    }

def range_meaningfulness(cluster_obj):
    ru = [i for i in cluster_obj if i['lang'] == 'ru']
    en = [i for i in cluster_obj if i['lang'] == 'en']

    ranged_ru = sorted(ru, key=lambda x: x['stats']['meaningfullness'])
    ranged_en = sorted(en, key=lambda x: x['stats']['meaningfullness'])

    return {
        'ru': {
            "low": [i['_id'] for i in ranged_ru[:5]],
            "high": [i['_id'] for i in ranged_ru[-5:]]
    }
    ,
        'en': {
            "low": [i['_id'] for i in ranged_en[:5]],
            "high": [i['_id'] for i in ranged_en[-5:]]
    }
    }

def range_bias(cluster_obj):
    ru = [i for i in cluster_obj if i['lang'] == 'ru']
    en = [i for i in cluster_obj if i['lang'] == 'en']

    ranged_ru = sorted(ru, key=lambda x: x['stats']['bias'])
    ranged_en = sorted(en, key=lambda x: x['stats']['bias'])

    return {
        'ru': {
            "low": [i['_id'] for i in ranged_ru[:5]],
            "high": [i['_id'] for i in ranged_ru[-5:]]
    }
    ,
        'en': {
            "low": [i['_id'] for i in ranged_en[:5]],
            "high": [i['_id'] for i in ranged_en[-5:]]
    }
    }

def summarize_keywords(cluster_obj):
    kwords = {
        'ru': [],
        'en': []
    }

    for article in cluster_obj:
        if article['lang'] == 'ru':
            kwords['ru'].extend(article['stats']['keywords'])
        elif article['lang'] == 'en':
            kwords['en'].extend(article['stats']['keywords'])
    
    c_ru = Counter(kwords['ru'])
    c_en = Counter(kwords['en'])

    return {
        'ru': c_ru.most_common(10),
        'en': c_en.most_common(10)
    }

def cluster_metrics(cluster_obj):
    publication_range = (min([i['article']['pub_date'] for i in cluster_obj]), max([i['article']['pub_date'] for i in cluster_obj]))
    ru_count = len([i for i in cluster_obj if i['lang'] == 'ru'])
    en_count = len([i for i in cluster_obj if i['lang'] == 'en'])

    return {
        "date_range": publication_range,
        "ru_count": ru_count,
        "en_count": en_count
    }

# corpus functions - MAYBE

# def sentiment_top(corpus):
#     return {}

# def meaningfullness_top(corpus):
#     return {}

# def bias_top(corpus):
#     return {}