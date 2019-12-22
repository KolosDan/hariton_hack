from scraper import get_top_articles
import json
from summa import keywords
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import time
from goslate import Goslate
from random import randint

gosl = Goslate()

lemmatizer = WordNetLemmatizer()

def get_en_query(cluster):
    kwrds = []
    for i in cluster:
        kwrds.extend([lemmatizer.lemmatize(w) for w in keywords.keywords(i['text'].lower()).split('\n') if w not in stopwords.words('russian')])
    
    c = Counter(kwrds)
    try:
        query = gosl.translate(' '.join([i[0] for i in c.most_common(5)]), 'en')
    except:
        time.sleep(randint(30,60))
        try:
            query = gosl.translate(' '.join([i[0] for i in c.most_common(5)]), 'en')
        except:
            query = input('Translator blocked: translate %s:\n>' % ' '.join([i[0] for i in c.most_common(5)]))
    url = 'https://news.google.com/search?q=%s&hl=en-US&gl=US&ceid=US:en' % query
    
    return url.replace(' ', '+')

def get_ru_query(cluster):
    kwrds = []
    for i in cluster:
        kwrds.extend([lemmatizer.lemmatize(w) for w in keywords.keywords(i['text'].lower()).split('\n') if w not in stopwords.words('english')])
    
    c = Counter(kwrds)
    try:
        query = gosl.translate(' '.join([i[0] for i in c.most_common(5)]), 'ru')
    except:
        time.sleep(randint(30,60))
        try:
            query = gosl.translate(' '.join([i[0] for i in c.most_common(5)]), 'ru')
        except:
            query = input('Translator blocked: translate %s:\n>' % ' '.join([i[0] for i in c.most_common(5)]))


    url = 'https://news.google.com/search?q=%s&hl=ru' % query
    return url.replace(' ', '+')
