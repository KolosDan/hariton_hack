from scraper import get_top_articles, get_mirror
from mirror import get_en_query, get_ru_query
from cleaner import clean
import json
from multiprocessing import Pool

ru_url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuSjFHZ0pTVlNnQVAB?hl=ru&gl=RU&ceid=RU%3Aru'
en_url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuSjFHZ0pTVlNnQVAB?hl=en-US&gl=US&ceid=US:en'

clean_ru_news = clean(get_top_articles(ru_url), 'russian')
clean_en_news = clean(get_top_articles(en_url), 'english')

news_corpus = []

p = Pool(len(clean_ru_news))
en_mirror_results = p.map(get_mirror, [get_en_query(block) for block in clean_ru_news])

for i in range(len(en_mirror_results)):
    news_corpus.append({
        'ru': clean_ru_news[i],
        'en': en_mirror_results[i]
    })

p = Pool(len(clean_en_news))
ru_mirror_results = p.map(get_mirror, [get_ru_query(block) for block in clean_en_news])

for i in range(len(ru_mirror_results)):
    news_corpus.append({
        'en': clean_en_news[i],
        'ru': ru_mirror_results[i]
    })


json.dump(big_clean(news_corpus), open('dump.json', 'w'))