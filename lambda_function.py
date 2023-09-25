import json
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

uri = os.getenv("URI")
db_name = os.getenv("DB")
collection_name = os.getenv("COLLECTION")
DEFAULT_LIMIT = 50
MAX_LIMIT = 300

def lambda_handler(event, context):
    
    # get the search text
    try:
        search_text = event['queryStringParameters']['search_text']
    except Exception as e:
        return {
            "Error Message": "Please add your search text value to 'search_text' key in the queryStringParameters"
        }
    
    # get the result limit    
    try:
        limit = int(event['queryStringParameters']['limit'])
        if limit > MAX_LIMIT:
            limit = MAX_LIMIT
    except:
        limit = DEFAULT_LIMIT
    
    try:
        # access the collection
        client = MongoClient(uri)
        collection = client[db_name][collection_name]
        
        # query the collection
        query = {"$text":{"$search": search_text}}
        query_result = [result for result in collection.find(query, {"_id": 0}).limit(limit)]
        
        # get result_count
        # result count might be less than the limit
        result_count = len(query_result)
        
        return {
            "result_count": result_count,
            "matched_results": query_result
        }
    except:
        return {
            "Error Message": "Couldn't connect to the database"
        }