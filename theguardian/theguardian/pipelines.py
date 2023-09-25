from itemadapter import ItemAdapter
from pymongo import MongoClient
import os

class TheguardianPipeline:
    
    def open_spider(self, spider):
        
        # get environment variables
        mongo_url = os.getenv('MONGODB_CONNECTION_URI')
        db_name = os.getenv('MONGODB_DB_NAME')
        db_collection = os.getenv('MONGODB_COLLECTION_NAME')

        # connect and get the desired collection
        self.mongo_client = MongoClient(mongo_url)
        self.collection = self.mongo_client[db_name][db_collection]

    def process_item(self, item, spider):
        
        # if the item exists, then update
        # else insert the item into the collection
        # item unique identifier is the uid found in the website DOM
        self.collection.update_one(
                {"uid":item['uid']},
                {"$set": item},
                upsert=True
            )
        return item

    def close_spider(self, spider):
        # close database connection
        self.mongo_client.close()