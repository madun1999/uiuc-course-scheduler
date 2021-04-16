from os import getenv
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def post_course_gpas(subject):
    """
    Add course gpas to database
    :param subject: the course gpas to add
    """
    client = MongoClient(getenv('MONGODB_KEY'))
    db = client[getenv('MONGODB_DB')]
    db['course_gpas'].replace_one({'course_id': subject['course_id']}, subject, upsert=True)
    client.close()