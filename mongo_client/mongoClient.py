import urllib.parse

from pymongo import MongoClient

password = urllib.parse.quote_plus('Passw0rdAintStr0ng')

cluster = MongoClient(
    'mongodb+srv://cs568user:{}@cluster0.ihgom.mongodb.net/<dbname>?retryWrites=true&w=majority'.format(password))

database = cluster['cs568-db']


class MongoRepository(object):
    def __init__(self):
        self.cluster = cluster
        self.database = database

    def add_url_schema(self, url_schema):
        urls_collection = self.database['urls']
        url_searched = urls_collection.find_one(url_schema)
        if url_searched is None:
            urls_collection.insert_one(url_schema)

    def add_url_fill_metadata_schema(self, url_fill_metadata_schema):
        url_fill_metadata_collection = self.database['url_fill_metadata']
        url_searched = url_fill_metadata_collection.find_one({'url': url_fill_metadata_schema['url']})
        if url_searched is None:
            url_fill_metadata_collection.insert_one(url_fill_metadata_schema)
        else:
            url_fill_metadata_collection.update_one({'url': url_fill_metadata_schema['url']}, {
                '$set': {'screenshot_differences': url_fill_metadata_schema['screenshot_differences'],
                         'inferred_affected_tuples': url_fill_metadata_schema['inferred_affected_tuples']}})
