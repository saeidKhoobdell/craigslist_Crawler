from abc import ABC,abstractmethod
import json

from mongo import MongoDatabase


class StorageAbstract(ABC):

      @abstractmethod
      def store(self):
        pass
      @abstractmethod
      def load(self):
        pass
      @abstractmethod
      def update(self):
        pass

class MongoStorage(StorageAbstract):

    def __init__(self):
        self.mongo = MongoDatabase()

    def store(self,data, collection, *args):
        collection = getattr(self.mongo.database, collection)
        if isinstance(data, list) and len(data) > 1:
            collection.insert_many(data)
        else :
          collection.insert_one(data)

    def load(self,collection_name, filter_name=None):
        collection =self.mongo.database[collection_name]
        if filter_name is not None:
            data = collection.find(filter_name)
        else :
            data = collection.find()
        return data

    def update(self, data):
        self.mongo.database.advertisement_links.find_one_and_update(
          {'_id': data['_id']},
          {'$set': {'flag':True}})


class FileStorage(StorageAbstract):

    def store(self, data, filename, *args):
        if type(data) == dict:
            filename = filename +'-'+data['post_id']
        # filename = filename +'-' + data['post_id']
        with open(f'fixtures/adv/{filename}.json', 'w') as f:
            f.write(json.dumps(data))

    def load(self,filename):
      with open(f'fixtures/adv/{filename}.json', 'r') as f:
        links = json.loads(f.read())
      return links

    def update(self):
      pass