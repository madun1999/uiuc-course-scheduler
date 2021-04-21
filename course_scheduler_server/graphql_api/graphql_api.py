import os

import dotenv
from ariadne import QueryType, graphql_sync, \
    make_executable_schema, load_schema_from_path, snake_case_fallback_resolvers, ObjectType, \
    convert_kwargs_to_snake_case
from typing import Any

from pymongo.errors import PyMongoError

import db.db_CIS_API_handler as database

from ariadne.constants import PLAYGROUND_HTML
from graphql import GraphQLResolveInfo
from pathlib import Path
from flask import Blueprint, request, abort, jsonify, current_app
from werkzeug.exceptions import BadRequest

from db.login import get_user, update_user
from scheduler.scheduler import schedule_courses
# from scheduler.scheduler_restriction import schedule_courses_with_restrictions
from google_auth.google_oauth import check_google_token
from scheduler.scheduler_restriction import RestrictionScheduler

dotenv.load_dotenv()

# flask blueprint
graphql_page = Blueprint('graphql_page', __name__)

STATUS_OK = 200
STATUS_BAD_REQUEST = 400
STATUS_BAD_PAYLOAD = 415


def _check_json_payload():
    """check if json payload is valid. Returns payload"""
    if not request.is_json:
        abort(STATUS_BAD_PAYLOAD, "Payload is not json.")
    try:
        payload = request.get_json()
        return payload
    except BadRequest:
        abort(STATUS_BAD_REQUEST, "Data is not valid json.")


# import graphql schema file
gql_types = load_schema_from_path(str(Path(os.getenv('UCS_PROJECT_ROOT'))
                                      / 'course_scheduler_server'
                                      / 'graphql_api'
                                      / 'schema.graphql'))


# graphql resolvers
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


def courses_resolver(*_, subject):
    """courses query. Gets all courses in a subject"""
    courses = database.get_courses_by_subject_id(subject)
    for course in courses:
        course.update({"subject_id": subject})
    return courses


def course_detail_resolver(obj, _):
    """courses query. Gets all courses in a subject"""
    detail = database.get_course_detail(obj['subject_id'], obj['course_num'])
    return detail


def section_course_resolver(obj, _):
    """section query. Get course."""
    section_id = obj["section_id"]
    course = database.get_course_from_section(section_id)
    course_id = course["course_id"]
    subject = course_id.split()[0]
    course_num = course_id.split()[1]
    return {"subject_id": subject, "course_num": course_num, "course_detail": course}


@convert_kwargs_to_snake_case
def course_resolver(*_, course_id):
    """courses query. Get one course with course id"""
    subject = course_id.split()[0]
    course_num = course_id.split()[1]
    course = database.get_course_detail(subject, course_num)
    return {"subject_id": subject, "course_num": course_num, "course_detail": course}


def user_resolver(_, info):
    """Query current user information."""
    cur_user = info.context["cur_user"]
    user = get_user(cur_user)
    user["id"] = user["_id"]

    return user

def user_stared_schedules_resolver(obj, _):
    stared_schedules = obj["stared_schedule_ids"]
    stared_schedules = [[database.get_section(section) for section in schedule]
                        for schedule in stared_schedules]
    return stared_schedules

def update_user_resolver(_, info):
    """Update current user information with current google token."""
    cur_user = info.context["cur_user"]
    update_user(cur_user)
    return {"success": True}


def schedule_resolver(*_, courses):
    """
    @deprecated
    courses is a list of  {"courseId": str, "mandatory": bool}
    """
    course_details = []
    for course_id in courses:
        subject = course_id.split()[0]
        course_num = course_id.split()[1]
        course_detail = database.get_course_detail(subject, course_num)
        if not course_detail:
            return {
                "success": False,
                "error": f"Course {course_id} does not exist."
            }
        course_details.append(course_detail)
    schedules, error = schedule_courses(course_details)
    if error:
        return {
            "success": False,
            "error": error
        }
    result = {
        "success": True,
        "schedules": [
            {"sections": schedule} for schedule in schedules
        ]
    }
    return result


def schedule_with_restrictions_resolver(*_, courses, restrictions):
    """
    courses is a list of  {"courseId": str, "mandatory": bool}
    restrictions is {"maxCourses": int, "minMandatory": int, breaks: [Break!]}
    `   where Break is {"start": str, "end": str, "days_of_the_week":
    """
    course_details = []
    max_courses = 100 if restrictions["maxCourses"] is None else restrictions["maxCourses"]
    min_mandatory = 0 if restrictions["minMandatory"] is None else restrictions["minMandatory"]
    breaks = [{"start": break1["start"], "end": break1["end"], "days_of_the_week": break1["daysOfTheWeek"]}
              for break1 in restrictions["breaks"]]

    for annotated_course in courses:
        course_id = annotated_course["courseId"]
        mandatory = annotated_course["mandatory"]
        subject = course_id.split()[0]
        course_num = course_id.split()[1]
        course_detail = database.get_course_detail(subject, course_num)
        if not course_detail:
            return {
                "success": False,
                "error": f"Course {course_id} does not exist."
            }
        course_details.append({"course": course_detail, "mandatory": mandatory})
    restriction_scheduler = RestrictionScheduler(max_courses, min_mandatory, breaks)
    schedules, error = restriction_scheduler.schedule_courses(course_details)
    if error:
        return {
            "success": False,
            "error": error
        }
    result = {
        "success": True,
        "schedules": [
            {"sections": schedule.to_list()} for schedule in schedules
        ]
    }
    return result

@convert_kwargs_to_snake_case
def star_schedule(_, info, section_ids):
    """
    Sections is a list of SectionIds / CRNs (int)
    """
    cur_user = info.context["cur_user"]
    user = get_user(cur_user)
    user["id"] = user["_id"]
    if "stared_schedule_ids" not in user:
        user["stared_schedule_ids"] = []
    user["stared_schedule_ids"].append(section_ids)
    update_user(user)
    return {"success": True}


# set up schema
query = QueryType()
query.set_field("subjects", subjects_resolver)
query.set_field("courses", courses_resolver)
query.set_field("course", course_resolver)
query.set_field("user", user_resolver)
query.set_field("schedule", schedule_resolver)
query.set_field("scheduleRestriction", schedule_with_restrictions_resolver)
course_query = ObjectType("Course")
course_query.set_field("courseDetail", course_detail_resolver)
section_query = ObjectType("Section")
section_query.set_field("course", section_course_resolver)
user_query = ObjectType("User")
user_query.set_field("staredSchedules", user_stared_schedules_resolver)
mutation = ObjectType("Mutation")
mutation.set_field("updateUser", update_user_resolver)
mutation.set_field("starSchedule", star_schedule)
schema = make_executable_schema(gql_types, query, course_query, section_query, user_query, mutation,
                                snake_case_fallback_resolvers)


# From ariadne flask tutorial
@graphql_page.route('/graphql', methods=["POST"])
def graphql_server():
    """The graphql endpoint"""
    data = _check_json_payload()
    try:
        cur_user = check_google_token()
    except ValueError as error:
        return "Authorization Error", STATUS_BAD_REQUEST
    success, result = graphql_sync(
        schema,
        data,
        context_value={"request": request, "cur_user": cur_user},
        debug=current_app.debug
    )
    status_code = STATUS_OK if success else STATUS_BAD_REQUEST
    return jsonify(result), status_code


# From ariadne flask tutorial
@graphql_page.route("/graphql", methods=["GET"])
def graphql_playground():
    """Graphql Explorer"""
    return PLAYGROUND_HTML, STATUS_OK
