import mongomock
import pymongo
from course_scheduler_server.db.section_handler import get_section
from os import getenv
from dotenv import load_dotenv

load_dotenv()


# db
@mongomock.patch(servers=getenv("MONGODB_CONNECT"))
def test_get_section_exist(app, client):
    sections = [
        {"section_id": 12345, "section_number": "ADB"}
    ]
    mongo_db = pymongo.MongoClient(getenv("MONGODB_CONNECT"))[getenv("MONGODB_DB")]
    mongo_db["sections"].insert_many(sections)
    section = get_section(12345)
    assert section["section_id"] == 12345
    assert section["section_number"] == "ADB"


@mongomock.patch(servers=getenv("MONGODB_CONNECT"))
def test_get_section_from_courses(app, client):
    section = {"section_id": 12345, "section_number": "ADB"}
    course = {"course_id": "CHOC100", "sections": [section]}
    mongo_db = pymongo.MongoClient(getenv("MONGODB_CONNECT"))[getenv("MONGODB_DB")]
    mongo_db["courses"].insert_one(course)

    actual_section = get_section(12345)
    assert actual_section["section_id"] == 12345
    assert actual_section["section_number"] == "ADB"
    stored_section = mongo_db["sections"].find_one({"section_id": 12345})
    assert stored_section["section_id"] == 12345
    assert stored_section["section_number"] == "ADB"


@mongomock.patch(servers=getenv("MONGODB_CONNECT"))
def test_get_section_fails(app, client):
    actual_section = get_section(12345)
    assert actual_section is None
