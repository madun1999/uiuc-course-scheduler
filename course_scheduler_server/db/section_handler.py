from os import getenv
from pymongo import MongoClient
from dotenv import load_dotenv

from CIS_API.fetch_course import fetch_course_from_CIS
from db.course_handler import get_course_from_section
from db.db_helper import find, find_one

load_dotenv()


def get_section_from_courses(section_id: int):
    """Get section by section_id from courses collection."""
    course = get_course_from_section(section_id)
    if course is None:
        return None
    matched_sections = filter(lambda sections: sections['section_id'] == section_id, course["sections"])
    return next(matched_sections)


def post_section(section):
    """Add section to sections collection"""
    client = MongoClient(getenv('MONGODB_KEY'))
    db = client[getenv('MONGODB_DB')]
    db['sections'].replace_one({'section_id': section['section_id']}, section, upsert=True)


def get_section(section_id: int):
    """Get section by section_id from sections collection. Add to sections collection if not exist"""
    section = find_one('sections', {'section_id': section_id})
    if section is None:
        section = get_section_from_courses(section_id)
        if section is None:
            return None
        post_section(section)
    return section


if __name__ == '__main__':
    get_section(64513)
