from flask import Flask, render_template, request
from pymongo import MongoClient
from summa import summarizer
from bson import ObjectId

client = MongoClient()
db = client.bipolarity

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feed')
def feed():
    # get posts: title, text summary, object_id
    clusters = []
    for cluster in list(db.clusters.find()):
        ru_pravda = db.articles.find_one({'_id': cluster['pravda']['ru']})
        en_pravda = db.articles.find_one({'_id': cluster['pravda']['en']})
        clusters.append({
            'id': str(cluster['_id']),
            'ru_title': ru_pravda['article']['title'],
            'ru_preview': summarizer.summarize(ru_pravda['article']['text'], language='russian'),
            'en_title': en_pravda['article']['title'],
            'en_preview': summarizer.summarize(en_pravda['article']['text'], language='english'),
            'metrics': cluster['cluster_metrics'],
            'tags': cluster['cluster_keywords']
        })
    return render_template('feed.html', clusters=clusters)

@app.route('/cluster/<cluster_id>')
def cluster(cluster_id):
    cluster = db.clusters.find_one({'_id': ObjectId(cluster_id)})
    output = {}
    output['_id'] = str(cluster['_id'])


    if request.args['range'] == "sentiment":
        output['high_range'] = list(zip([db.articles.find_one({'_id': i})['article'] for i in cluster['sentiment_range']['ru']['high']], [db.articles.find_one({'_id': i})['article'] for i in cluster['sentiment_range']['en']['high']] ))
        output['low_range'] = list(zip([db.articles.find_one({'_id': i})['article'] for i in cluster['sentiment_range']['ru']['low']], [db.articles.find_one({'_id': i})['article'] for i in cluster['sentiment_range']['en']['low']] ))
    elif request.args['range'] == 'bias':
        output['high_range'] = list(zip([db.articles.find_one({'_id': i})['article'] for i in cluster['bias_range']['ru']['high']], [db.articles.find_one({'_id': i})['article'] for i in cluster['bias_range']['en']['high']] ))
        output['low_range'] = list(zip([db.articles.find_one({'_id': i})['article'] for i in cluster['bias_range']['ru']['low']], [db.articles.find_one({'_id': i})['article'] for i in cluster['bias_range']['en']['low']] ))
    elif request.args['range'] == 'meaningfullness':
        output['high_range'] = list(zip([db.articles.find_one({'_id': i})['article'] for i in cluster['meaningfullness_range']['ru']['high']], [db.articles.find_one({'_id': i})['article'] for i in cluster['meaningfullness_range']['en']['high']] ))
        output['low_range'] = list(zip([db.articles.find_one({'_id': i})['article'] for i in cluster['meaningfullness_range']['ru']['low']], [db.articles.find_one({'_id': i})['article'] for i in cluster['meaningfullness_range']['en']['low']] ))
  
    ru_pravda = db.articles.find_one({'_id': cluster['pravda']['ru']})
    en_pravda = db.articles.find_one({'_id': cluster['pravda']['en']})
    output['ru_pravda'] = ru_pravda['article']
    output['en_pravda'] = en_pravda['article']

    output['ru_count'] = cluster['cluster_metrics']['ru_count']
    output['en_count'] = cluster['cluster_metrics']['en_count']
    
    return render_template('cluster.html', ObjectId=ObjectId, output=output)


if __name__ == '__main__':
    app.run(host='0.0.0.0')