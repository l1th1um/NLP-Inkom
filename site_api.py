#!/home/arozie/crawler_env/bin/python3.6
from flask import Flask, render_template, request
import pymongo
from pymongo import MongoClient
import re
import json
from flask_cors import CORS, cross_origin
import random
from bson import json_util

from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

client = MongoClient()
db = client.event_detection
tweet = db.tweet
media = db.media
media_tagged = db.media_tagged


@app.route("/", methods=['GET', 'POST'])
def home():
    return "This Is Sparta"

@app.route("/total_tweet", methods=['GET'])
def total_tweet():
    return json.dumps({'total' : tweet.count()})

@app.route("/total_news/<string:news_portal>", methods=['GET'])
def total_news(news_portal):
    data = media.find({'portal' : news_portal})
    return json.dumps({'total' : data.count()})

@app.route("/last_crawled_news/<string:news_portal>", methods=['GET'])
def last_crawled_news(news_portal):    
    data = media.find_one({'portal' : news_portal}, { "crawled_at": 1, "_id" :0 }, sort=[('crawled_at', pymongo.DESCENDING)], limit=1)

    return json.dumps({'last_crawl' : data['crawled_at'].strftime("%d/%m/%Y %H:%M")})   

@app.route("/auto_tag", methods=['GET'])
def auto_tag():
    total = media_tagged.count() 
    # data = media_tagged.find('skip=' + str(random.randrange(0, total)))
    # data = media_tagged.find_one({'sentence' : 1}, skip=2)
    data = media_tagged.find_one(skip=random.randrange(0, total))

    return JSONEncoder().encode(data)
    

@app.route("/auto_tag_twitter", methods=['GET'])
def auto_tag_twitter():
    total = media_tagged.count() 
    # data = media_tagged.find('skip=' + str(random.randrange(0, total)))
    # data = media_tagged.find_one({'sentence' : 1}, skip=2)
    data = media_tagged.find_one(skip=random.randrange(0, total))

    return JSONEncoder().encode(data)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8113)
