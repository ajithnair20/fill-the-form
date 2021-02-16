import json

import bson
from flask import make_response
import nltk
from textblob import TextBlob

def getSentenceSentiment(sent):
    blob = TextBlob(sent)
    pol = blob.sentiment.polarity
    if pol >= 0:
        return 'pos'
    else:
        return 'neg'


def json_response(obj, cls=None):
    response = make_response(json.dumps(obj, cls=cls))
    response.content_type = 'application/json'

    return response


class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bson.ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
