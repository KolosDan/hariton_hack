from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient()
db = client.bipolarity

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feed')
def feed():
    return render_template('feed.html')

@app.route('/cluster/<cluster_id>')
def cluster(cluster_id):
    return render_template('cluster.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')