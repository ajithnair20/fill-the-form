# import patterns as pt
import nltk
from nltk.tag.stanford import StanfordPOSTagger
from nltk.tokenize import word_tokenize
import re
import os


# ------------------------------------------------------------------------------------------
# Username extraction using POS tagging
# message = 'ajithnair is not available. Try ajithnair20 instead'
# prev = 'ajithnair'
# print(pt.getUsername(message,prev))

# dirname = os.path.dirname(__file__)
# filename = os.path.join(dirname, '../corenlp/stanford-postagger-full-2020-11-17/stanford-postagger.jar')
# print(dirname)

# ------------------------------------------------------------------------------------------
# Text generation using regex patterns
# from xeger import Xeger

# regex_str = '((0?[1-9])|([12][0-9])|(3[01]))'
# x = Xeger()
# op = x.xeger(regex_str)
# print(op)
# msg = 'Enter mnumber in formt xxx-xxx-xxxx'
# print(pt.getPhoneNumberInput(msg))

# ------------------------------------------------------------------------------------------
# Sentiment analysis using nltk
# import nltk
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from nltk import tokenize
# from textblob import TextBlob
# sentences = '''
# Username is available
# '''
# blob = TextBlob(sentences)
# print(blob.tags)
# print(blob.noun_phrases)
# for sentence in blob.sentences:
#     print(sentence.sentiment.polarity)

# ------------------------------------------------------------------------------------------
# Keyword extraction using nltk
# from rake_nltk import Rake
# r = Rake() # Uses stopwords for english from NLTK, and all puntuation characters.

# r.extract_keywords_from_text('Age cannot be blank')

# print(r.get_ranked_phrases_with_scores()) # To get keyword phrases ranked highest to lowest.