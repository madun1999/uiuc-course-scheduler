# environment variables & path
import os
import dotenv
from pathlib import Path
# ariadne graphql
from ariadne import graphql_sync, \
    make_executable_schema, load_schema_from_path, snake_case_fallback_resolvers
from ariadne.constants import PLAYGROUND_HTML
# flask server & googleauthentication
from flask import Blueprint, request, jsonify, current_app
from google_auth.google_oauth import check_google_token

# graphql bindables
from graphql_api.star_schedule import star_schedule_binds
from graphql_api.user import user_binds
from graphql_api.course_info import course_info_binds
from graphql_api.scheduler import scheduler_binds
from tools import _check_json_payload, STATUS_OK, STATUS_BAD_REQUEST

# load dotenv
dotenv.load_dotenv()

# flask blueprint
graphql_page = Blueprint('graphql_page', __name__)

# import graphql schema file
gql_types = load_schema_from_path(str(Path(os.getenv('UCS_PROJECT_ROOT'))
                                      / 'course_scheduler_server'
                                      / 'graphql_api'
                                      / 'schema.graphql'))

# set up schema
schema = make_executable_schema(gql_types, *course_info_binds, *user_binds,
                                *scheduler_binds, *star_schedule_binds,
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
