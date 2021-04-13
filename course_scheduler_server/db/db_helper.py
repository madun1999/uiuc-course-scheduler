"""
A module for communication with the mongo database.
Mostly wrappers around mongo collection functions.
Copied from assignment2
"""
import pymongo
from dotenv import load_dotenv
from os import getenv

# load environment variables
load_dotenv()
print(getenv("MONGODB_CONNECT"))


def find(collection, query=None):
    """
    Wrapper around collection.find. Return list of items get.
    Leave query = None to get all items in the collections.
    """
    mongo_client = pymongo.MongoClient(getenv("MONGODB_CONNECT"))
    mongo_db = mongo_client[getenv("MONGODB_DB")]
    if query is None:
        query = dict()
    cursor = mongo_db[collection].find(query)
    return list(cursor)


def has_key(collection, key):
    """If the collection has the key"""
    return len(find(collection, {"_id": key})) > 0


def delete_one(collection, query):
    """Delete an id from the collection"""
    mongo_client = pymongo.MongoClient(getenv("MONGODB_CONNECT"))
    mongo_db = mongo_client[getenv("MONGODB_DB")]
    mongo_db[collection].delete_one(query)


def replace_one(collection, query, item, upsert=True):
    """wrapper around replace_one"""
    mongo_client = pymongo.MongoClient(getenv("MONGODB_CONNECT"))
    mongo_db = mongo_client[getenv("MONGODB_DB")]
    mongo_db[collection].replace_one(query, item, upsert=upsert)


def replace_one_with_key(collection, key, item, upsert=True):
    """wrapper around replace_one with key"""
    mongo_client = pymongo.MongoClient(getenv("MONGODB_CONNECT"))
    mongo_db = mongo_client[getenv("MONGODB_DB")]
    mongo_db[collection].replace_one({"_id": key}, item, upsert=upsert)


def set_fields(collection, use_id, update_item):
    """Wrapper around collection.update that sets stuff."""
    mongo_client = pymongo.MongoClient(getenv("MONGODB_CONNECT"))
    mongo_db = mongo_client[getenv("MONGODB_DB")]
    result = mongo_db[collection].update_one({"_id": use_id},
                                             {"$set": update_item})