from typing import Any

import mongomock
import pymongo
from course_scheduler_server.db.gpa_handler import get_section_gpa, NO_GPA_SECTION
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# db
@mongomock.patch(servers=getenv("MONGODB_CONNECT"))
def test_get_section_gpa_exist(app, client):
    section = {
        "section_id": 12347,
        "section_number": "ADB",
        "meetings": [{
            "instructors": [{"first_name": "L", "last_name": "Sharif"}]
        }],
        "gpa": {
            "average": 3.181,
            "a_rate": 0.534,
        }
    }

    mongo_db = pymongo.MongoClient(getenv("MONGODB_CONNECT"))[getenv("MONGODB_DB")]
    mongo_db["sections"].insert_one(section)
    actual_gpa = get_section_gpa(12347)
    assert actual_gpa["average"] == 3.181
    assert actual_gpa["a_rate"] == 0.534

@mongomock.patch(servers=getenv("MONGODB_CONNECT"))
def test_get_section_gpa_from_course_gpas(app, client):
    section = {
        "section_id": 12348,
        "section_number": "ADB",
        "meetings": [{
            "instructors": [{"first_name": "L", "last_name": "Sharif"}]
        }]
    }
    course = {"course_id": "CHOC101", "sections": [section]}
    course_gpa = {
        "course_id": "CHOC101",
        "instructor_grades": [{
            "first_name": "Lila A",
            "last_name": "Sharif",
            "mean_grades": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        }]
    }
    mongo_db = pymongo.MongoClient(getenv("MONGODB_CONNECT"))[getenv("MONGODB_DB")]
    mongo_db["courses"].insert_one(course)
    mongo_db["sections"].insert_one(section)
    mongo_db["course_gpas"].insert_one(course_gpa)

    actual_gpa = get_section_gpa(12348)
    assert actual_gpa["average"] == 2.119285714285714
    assert actual_gpa["a_rate"] == 1 / 7
    stored_section = mongo_db["sections"].find_one({"section_id": 12348})
    assert stored_section["gpa"]["average"] == 2.119285714285714
    assert stored_section["gpa"]["a_rate"] == 1 / 7

@mongomock.patch(servers=getenv("MONGODB_CONNECT"))
def test_get_section_gpa_from_course_gpas_add_section(app, client):
    section = {
        "section_id": 12349,
        "section_number": "ADB",
        "meetings": [{
            "instructors": [{"first_name": "L", "last_name": "Sharif"}]
        }]
    }
    course = {"course_id": "CHOC109", "sections": [section]}
    course_gpa = {
        "course_id": "CHOC109",
        "instructor_grades": [{
            "first_name": "Lila A",
            "last_name": "Sharif",
            "mean_grades": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        }]
    }
    mongo_db = pymongo.MongoClient(getenv("MONGODB_CONNECT"))[getenv("MONGODB_DB")]
    mongo_db["courses"].insert_one(course)
    mongo_db["course_gpas"].insert_one(course_gpa)
    actual_gpa = get_section_gpa(12349)
    assert actual_gpa["average"] == 2.119285714285714
    assert actual_gpa["a_rate"] == 1 / 7
    stored_section = mongo_db["sections"].find_one({"section_id": 12349})
    assert stored_section["section_id"] == 12349
    assert stored_section["section_number"] == "ADB"
    assert stored_section["gpa"]["average"] == 2.119285714285714
    assert stored_section["gpa"]["a_rate"] == 1 / 7


@mongomock.patch(servers=getenv("MONGODB_CONNECT"))
def test_get_section_gpa_from_course_no_match_name(app, client):
    section = {
        "section_id": 12340,
        "section_number": "ADB",
        "meetings": [{
            "instructors": [{"first_name": "L", "last_name": "Sharif"}]
        }]
    }
    course = {"course_id": "CHOC102", "sections": [section]}
    course_gpa = {
        "course_id": "CHOC102",
        "instructor_grades": [{
            "first_name": "Flora A",
            "last_name": "Sharif",
            "mean_grades": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        }]
    }
    mongo_db = pymongo.MongoClient(getenv("MONGODB_CONNECT"))[getenv("MONGODB_DB")]
    mongo_db["courses"].insert_one(course)
    mongo_db["sections"].insert_one(section)
    mongo_db["course_gpas"].insert_one(course_gpa)

    actual_gpa = get_section_gpa(12340)
    assert actual_gpa is None
    stored_section = mongo_db["sections"].find_one({"section_id": 12340})
    assert stored_section["gpa"] == NO_GPA_SECTION


@mongomock.patch(servers=getenv("MONGODB_CONNECT"))
def test_get_section_gpa_not_exist(app, client):
    section = {
        "section_id": 12370,
        "section_number": "ADB",
        "meetings": [{
            "instructors": [{"first_name": "L", "last_name": "Sharif"}]
        }]
    }
    course = {"course_id": "CHOC105", "sections": [section]}
    course_gpa = {
        "course_id": "CHOC105",
        "instructor_grades": [{
            "first_name": "Lila A",
            "last_name": "Sharif",
            "mean_grades": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        }]
    }

    mongo_db = pymongo.MongoClient(getenv("MONGODB_CONNECT"))[getenv("MONGODB_DB")]
    mongo_db["courses"].insert_one(course)
    mongo_db["sections"].insert_one(section)
    mongo_db["course_gpas"].insert_one(course_gpa)

    actual_gpa = get_section_gpa(12380)
    assert actual_gpa is None
    stored_section = mongo_db["sections"].find_one({"section_id": 12380})
    assert stored_section is None


@mongomock.patch(servers=getenv("MONGODB_CONNECT"))
def test_get_section_gpa_course_not_exist(app, client):
    section = {
        "section_id": 12342,
        "section_number": "ADB",
        "meetings": [{
            "instructors": [{"first_name": "L", "last_name": "Sharif"}]
        }]
    }
    course_gpa = {
        "course_id": "CHOC107",
        "instructor_grades": [{
            "first_name": "Lila A",
            "last_name": "Sharif",
            "mean_grades": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        }]
    }
    mongo_db = pymongo.MongoClient(getenv("MONGODB_CONNECT"))[getenv("MONGODB_DB")]
    mongo_db["sections"].insert_one(section)
    mongo_db["course_gpas"].insert_one(course_gpa)

    actual_gpa = get_section_gpa(12342)
    assert actual_gpa is None
    stored_section = mongo_db["sections"].find_one({"section_id": 12342})
    assert stored_section["gpa"] == NO_GPA_SECTION
