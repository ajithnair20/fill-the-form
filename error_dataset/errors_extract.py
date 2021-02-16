import json
import nltk
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
import os
from bs4 import BeautifulSoup as bs
import csv



# Source: http://blog.alejandronolla.com/2013/05/15/detecting-text-language-with-python-and-nltk/
def _calculate_languages_ratios(text):
    languages_ratios = {}
    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    # Compute per language included in nltk number of unique stopwords appearing in analyzed text
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements) # language "score"

    return languages_ratios


#----------------------------------------------------------------------
def detect_language(text):
    ratios = _calculate_languages_ratios(text)

    most_rated_language = max(ratios, key=ratios.get)

    return most_rated_language


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'url_fill_metadata_collection.json')
op_filename = os.path.join(dirname, 'errors.txt')


def get_tag_from_string(htmlStr: str, element_type: str):
    soup = bs(htmlStr, 'html.parser')
    tag = soup.find(element_type)
    return tag

# Extracting error messages
f = open(filename,'r',encoding='UTF-8')
lines  = f.readlines()
errors = []
for line in lines:
    ip = json.loads(str(line))
    errors.extend(ip['screenshot_differences'])

print(f'Number of error messages: {len(errors)}')

# Extracting input elements
inputs = []
for line in lines:
    ip = json.loads(str(line))
    tup = ip['inferred_affected_tuples']

    for t in tup:
        elem = t['affected_input']
        inputs.append(elem)

print(f'Number of input elements: {len(inputs)}')

attr_map = {}

for i in inputs:
    elem = get_tag_from_string(i,'input')
    attributes = elem.attrs
    for attr in attributes:
        if attr in attr_map:
            attr_map[attr] += 1
        else:
            attr_map[attr] = 1

sorted_attr_map = dict(sorted(attr_map.items(), key=lambda item: item[1], reverse=True))
print(sorted_attr_map)

# Writing attributes to external file
csv_columns = ['Attribute','Count']
csv_file = os.path.join(dirname, 'attributes.csv')

c = open(csv_file, 'w')
c.write("Attributes,WebsiteCount")
c.write("")
for key in sorted_attr_map.keys():
    c.write("%s,%s\n"%(key,sorted_attr_map[key]))
c.close()

# Writing erorrs to external file
op = open(op_filename,'w', encoding='UTF-8')
for error in errors:
    language = detect_language(error)
    if language == 'english':
        op.write(error)
        op.write('\n')

op.close()
f.close()