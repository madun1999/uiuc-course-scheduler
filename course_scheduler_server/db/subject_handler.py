from os import getenv

from pymongo import MongoClient

from db.db_helper import find


def post_subject(subject):
    """
    Add a subject to database
    :param subject: the subject to add
    """
    client = MongoClient(getenv('MONGODB_KEY'))
    db = client[getenv('MONGODB_DB')]
    db['subjects'].replace_one({'subject_id': subject['subject_id']}, subject, upsert=True)


def post_subject_courses(subject_courses):
    """
    Add a subject courses to database
    :param subject_courses: the subject courses to add
    """
    client = MongoClient(getenv('MONGODB_KEY'))
    db = client[getenv('MONGODB_DB')]
    db['subject_courses'].replace_one({'subject_id': subject_courses['subject_id']}, subject_courses, upsert=True)


def get_all_subjects():
    """Get all subjects from db"""
    all_subjects_obj = find('subjects', {})
    return [subject for subject in all_subjects_obj]