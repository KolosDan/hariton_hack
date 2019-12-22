from scraper import get_top_articles
import json
from summa import keywords
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import requests
import time

def translate(text, lang):
    try:
        response = requests.get("https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20191221T075558Z.44eb038ba8d8b45d.912f1c0533276f6b1e0b19fb777d96842da7befa&text=%s&lang=%s" % (text, lang)).json()['text'][0]
        return response
    except KeyError:
        return ''

lemmatizer = WordNetLemmatizer()

def get_en_query(cluster):
    kwrds = []
    for i in cluster:
        kwrds.extend([lemmatizer.lemmatize(w) for w in keywords.keywords(i['text'].lower()).split('\n') if w not in stopwords.words('russian')])
    
    c = Counter(kwrds)
    query = ''
    for i in c.most_common(5):
        query += translate(i[0], 'en') + '+'
        time.sleep(1)
    
    url = 'https://news.google.com/search?q=%s&hl=en-US&gl=US&ceid=US:en' % query
    
    return url.replace(' ', '+')

def get_ru_query(cluster):
    kwrds = []
    for i in cluster:
        kwrds.extend([lemmatizer.lemmatize(w) for w in keywords.keywords(i['text'].lower()).split('\n') if w not in stopwords.words('english')])
    
    c = Counter(kwrds)
    query = ''
    for i in c.most_common(5):
        query += translate(i[0], 'ru') + '+'
        time.sleep(1)
    url = 'https://news.google.com/search?q=%s&hl=ru' % query
    
    return url.replace(' ', '+')
