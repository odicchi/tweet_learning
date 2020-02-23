from pymongo import MongoClient

class MongoDAO(object):

    def __init__(self, dbName, collectionName):
        self.client = MongoClient()
        self.db = self.client[dbName] #DB名を設定
        self.collection = self.db.get_collection(collectionName)

    def find_one(self, projection=None,filter=None, sort=None):
        return self.collection.find_one(projection=projection,filter=filter,sort=sort)

    def find(self, projection=None,filter=None, sort=None):
        return self.collection.find(projection=projection,filter=filter,sort=sort, no_cursor_timeout=True)

    def count_documents(self, filter=None):
        return self.collection.count_documents(filter)

    def insert_one(self, document):
        return self.collection.insert_one(document)

    def insert_many(self, documents):
        return self.collection.insert_many(documents)

    def update_one(self, filter, update):
        return self.collection.update_one(filter,update)

    def update_many(self, filter, update):
        return self.collection.update_many(filter,update)

    def replace_one(self, filter, replacement):
        return self.collection.replace_one(filter, replacement)

    def find_one_and_replace(self, filter, replacement):
        return self.collection.find_one_and_replace(filter, replacement)

    def aggregate(self, filter, **keyword):
        return self.collection.aggregate(filter, keyword)

    def delete_one(self, filter):
        return self.collection.delete_one(filter)

    def delete_many(self, filter):
        return self.collection.delete_many(filter)

    def find_one_and_delete(self, filter):
        return self.collection.find_one_delete(filter)