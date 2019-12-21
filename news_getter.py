from scraper import get_top_articles, get_mirror
from mirror import get_en_query, get_ru_query
from cleaner import clean
import json

ru_url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuSjFHZ0pTVlNnQVAB?hl=ru&gl=RU&ceid=RU%3Aru'
en_url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuSjFHZ0pTVlNnQVAB?hl=en-US&gl=US&ceid=US:en'

clean_ru_news = clean(get_top_articles(ru_url), 'russian')
clean_en_news = clean(get_top_articles(en_url), 'english')

news_corpus = []

for block in clean_ru_news:
    mirror_en_news = get_mirror(get_en_query(block))
    sample = {
        'ru': clean_ru_news,
        'en': mirror_en_news
    }
    news_corpus.append(sample)


for block in clean_en_news:
    mirror_ru_news = get_mirror(get_ru_query(block))
    sample = {
        'ru': mirror_ru_news,
        'en': block
    }
    news_corpus.append(sample)

json.dump(news_corpus, open('dump.json', 'w'))