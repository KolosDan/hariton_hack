from scraper import get_top_articles, get_mirror
from mirror import get_en_query, get_ru_query
from cleaner import clean, big_clean
import json
from multiprocessing import Pool
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

ru_url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuSjFHZ0pTVlNnQVAB?hl=ru&gl=RU&ceid=RU%3Aru'
en_url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuSjFHZ0pTVlNnQVAB?hl=en-US&gl=US&ceid=US:en'

print('%s [INFO] STARTED GATHERING NEWS CORPUS' % str(datetime.now()))


clean_ru_news = clean(get_top_articles(ru_url), 'russian')
clean_en_news = clean(get_top_articles(en_url), 'english')

news_corpus = []

print('%s [INFO] STARTED MIRROR GATHERING' % str(datetime.now()))

p = Pool(len(clean_ru_news))
en_queries = [get_en_query(block) for block in clean_ru_news]

print('%s [INFO] STARTED RU->EN MIRRORING' % str(datetime.now()))
en_mirror_results = p.map(get_mirror, en_queries)

for i in range(len(en_mirror_results)):
    news_corpus.append({
        'ru': clean_ru_news[i],
        'en': en_mirror_results[i]
    })
print('%s [INFO] FINISHED RU->EN MIRRORING' % str(datetime.now()))

p = Pool(len(clean_en_news))
ru_queries = [get_ru_query(block) for block in clean_en_news]

print('%s [INFO] STARTED EN->RU MIRRORING' % str(datetime.now()))
ru_mirror_results = p.map(get_mirror, ru_queries)

for i in range(len(ru_mirror_results)):
    news_corpus.append({
        'en': clean_en_news[i],
        'ru': ru_mirror_results[i]
    })
print('%s [INFO] FINISHED EN->RU MIRRORING' % str(datetime.now()))

print('%s [INFO] STARTED BIG CLEAN' % str(datetime.now()))

final_corpus = big_clean(news_corpus)

json.dump(final_corpus, open('corpus.json'))

# client = MongoClient()

# db = client.bipolarity

# for cluster in final_corpus:
#     item_ids = []
#     for lang in cluster:
#         for article in cluster[lang]:
#             item_ids.append(db.articles.insert_one({'article': article, 'lang': lang, 'stats': None}).inserted_id)

#     db.clusters.insert_one({
#         'articles': item_ids,
#         'pravda': None,
#         'sentiment_range': None,
#         'meaningfullness_range': None,
#         'bias_range': None,
#         'cluster_metrics': None
#     })

