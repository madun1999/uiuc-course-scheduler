from ariadne import QueryType, graphql_sync, \
    make_executable_schema, load_schema_from_path, snake_case_fallback_resolvers, ObjectType, \
    convert_kwargs_to_snake_case
from typing import Any
from graphql import GraphQLResolveInfo
import db.db_CIS_API_handler as database
from pymongo.errors import PyMongoError


query = QueryType()
course_query = ObjectType("Course")
section_query = ObjectType("Section")
course_info_binds = [query, course_query, section_query]


@query.field("subjects")
def subjects_resolver(obj: Any, info: GraphQLResolveInfo):
    """subjects query. Gets all subjects."""
    try:
        all_subjects = database.get_all_subjects()
    except (ValueError, PyMongoError) as e:
        return {
            "success": False,
            "error": str(e),
        }
    return {
        "success": True,
        "result": all_subjects,
    }


@query.field("courses")
def courses_resolver(*_, subject):
    """courses query. Gets all courses in a subject"""
    courses = database.get_courses_by_subject_id(subject)
    for course in courses:
        course.update({"subject_id": subject})
    return courses


@query.field("course")
@convert_kwargs_to_snake_case
def course_resolver(*_, course_id):
    """courses query. Get one course with course id"""
    subject = course_id.split()[0]
    course_num = course_id.split()[1]
    return {"subject_id": subject, "course_num": course_num}


@course_query.field("courseDetail")
def course_detail_resolver(obj, _):
    """courses query. Gets all courses in a subject"""
    detail = database.get_course_detail(obj['subject_id'], obj['course_num'])
    return detail


@section_query.field("course")
def section_course_resolver(obj, _):
    """section query. Get course."""
    section_id = obj["section_id"]
    course = database.get_course_from_section(section_id)
    course_id = course["course_id"]
    subject = course_id.split()[0]
    course_num = course_id.split()[1]
    return {"subject_id": subject, "course_num": course_num, "course_detail": course}
