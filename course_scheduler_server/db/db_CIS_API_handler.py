from os import getenv
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def post_subject(subject):
    """
    Add a subject to database
    :param subject: the subject to add
    """
    client = MongoClient(getenv('MONGODB_KEY'))
    db = client[getenv('MONGODB_DB')]
    db['subjects'].replace_one({'subject_id': subject['subject_id']}, subject, upsert=True)
    client.close()


def post_subject_courses(subject_courses):
    """
    Add a subject courses to database
    :param subject_courses: the subject courses to add
    """
    client = MongoClient(getenv('MONGODB_KEY'))
    db = client[getenv('MONGODB_DB')]
    db['subject_courses'].replace_one({'subject_id': subject_courses['subject_id']}, subject_courses, upsert=True)
    client.close()


def post_course(course):
    """
    Add a course to database
    :param course: the course to add
    """
    client = MongoClient(getenv('MONGODB_KEY'))
    db = client[getenv('MONGODB_DB')]
    db['courses'].replace_one({'course_id': course['course_id']}, course, upsert=True)
    client.close()

