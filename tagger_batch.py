from pymongo import MongoClient
from nltk.tokenize import sent_tokenize
from idnlp import PoSTagger
# from bson import Int64
from bson import objectid
import pprint


pos_tagger = PoSTagger()

client = MongoClient('mongodb://localhost:27017/')

db = client.event_detection

for post in db.media.find({'portal' : 'antara'}):		
	sent_list = sent_tokenize(post['content'])
			
	for sentence in sent_list:
		tagged = {"media_id" : objectid.ObjectId(post['_id'])}
		tagged['sentence'] = sentence
		tagged['auto_tag'] = pos_tagger.predict(sentence)
		db.media_tagged.insert(tagged, check_keys=False)