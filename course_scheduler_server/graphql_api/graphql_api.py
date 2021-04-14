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
from google_auth.google_oauth import check_google_token

dotenv.load_dotenv()

# flask blueprint
graphql_page = Blueprint('graphql_page', __name__)

STATUS_OK = 200
STATUS_BAD_REQUEST = 400


def _check_json_payload():
    """check if json payload is valid. Returns payload"""
    if not request.is_json:
        abort(415, "Payload is not json.")
    try:
        payload = request.get_json()
        return payload
    except BadRequest:
        abort(400, "Data is not valid json.")


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


def update_user_resolver(_, info):
    """Update current user information with current google token."""
    cur_user = info.context["cur_user"]
    update_user(cur_user)
    return {"success": True}


def schedule_resolver(*_, courses):
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


# set up schema
query = QueryType()
query.set_field("subjects", subjects_resolver)
query.set_field("courses", courses_resolver)
query.set_field("course", course_resolver)
query.set_field("user", user_resolver)
course = ObjectType("Course")
course.set_field("courseDetail", course_detail_resolver)
mutation = ObjectType("Mutation")
mutation.set_field("updateUser", update_user_resolver)
schema = make_executable_schema(gql_types, query, course, mutation, snake_case_fallback_resolvers)


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
