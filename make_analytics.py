import json
from pymongo import MongoClient
from datetime import datetime
from analysis import get_article_stats, get_pravda, range_bias, range_meaningfulness, range_sentiment, cluster_metrics, summarize_keywords

final_corpus = json.load(open('corpus.json'))

client = MongoClient()
db = client.bipolarity

print('%s [INFO] STARTED CORPUS ANALYSIS' % str(datetime.now()))

for index, cluster in enumerate(final_corpus):
    print('%s [INFO] ANALYZING %s OUT OF %s CLUSTERS' % (str(datetime.now()), str(index+1), str(len(final_corpus))))
    item_ids = []
    for lang in cluster:
        for article in cluster[lang]:
            stats = get_article_stats({'article': article, 'lang': lang})
            item_ids.append(db.articles.insert_one({'article': article, 'lang': lang, 'stats': stats}).inserted_id)

    cluster_obj = list(db.articles.find({'_id': {'$in': item_ids}}))
    print('FINISHED - GETTING CLUSTER STATS')
    db.clusters.insert_one({
        'articles': item_ids,
        'pravda': get_pravda(cluster_obj),
        'sentiment_range': range_sentiment(cluster_obj),
        'meaningfullness_range': range_meaningfulness(cluster_obj),
        'bias_range': range_bias(cluster_obj),
        'cluster_metrics': cluster_metrics(cluster_obj),
        'cluster_keywords': summarize_keywords(cluster_obj)
    })

client.close()

