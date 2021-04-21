from os import getenv
from pymongo import MongoClient
from dotenv import load_dotenv

from CIS_API.fetch_course import fetch_course_from_CIS
from db.db_helper import find, find_one

load_dotenv()


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


def post_course(course):
    """
    Add a course to database
    :param course: the course to add
    """
    client = MongoClient(getenv('MONGODB_KEY'))
    db = client[getenv('MONGODB_DB')]
    db['courses'].replace_one({'course_id': course['course_id']}, course, upsert=True)


def get_all_subjects():
    """Get all subjects from db"""
    all_subjects_obj = find('subjects', {})
    return [subject for subject in all_subjects_obj]


def add_course_to_db(subject_id, course_num, year_semester='2021/fall/'):
    """
    :param subject_id: subject id, i.e. 'CS'
    :param course_num: course number, i.e. '233'
    :param year_semester: year semester, i.e. '2021/fall/'
    :return: add the parsed course into database
    """
    parsed_course = fetch_course_from_CIS(f"{subject_id}/{course_num}", year_semester)
    if parsed_course is not False:
        post_course(parsed_course)
    else:
        return False


def get_courses_by_subject_id(subject: str):
    """Get all courses from db"""
    subject_courses = find_one('subject_courses', {'subject_id': subject})
    return subject_courses['courses']


def get_course_detail(subject_id: str, course_num):
    """Get course detail from db"""
    course_id = f"{subject_id} {course_num}"
    course_detail = find_one('courses', {'course_id': course_id})
    if not course_detail:
        add_course_to_db(subject_id, course_num)
        course_detail = find_one('courses', {'course_id': course_id})
    return course_detail


