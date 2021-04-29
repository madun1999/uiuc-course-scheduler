"""API Server"""
from json import dumps
from google_auth.google_oauth import check_google_token
from db.login import deactivate, get_user, sign_up, user_exist
from flask import Flask
from flask_cors import CORS
from pymongo.errors import PyMongoError
from graphql_api.graphql_api import graphql_page
from tools import STATUS_OK, STATUS_BAD_REQUEST
# the app
app = Flask(__name__)
# CORS
CORS(app)


def wrap_response(result):
    """create response, abort if error"""
    return result[1], result[0]


# login
@app.route('/api/login', methods=["POST"])
def login_user():
    try:
        user = check_google_token()
        if user_exist(user):
            return "Logged in", STATUS_OK
        else:
            sign_up(user)
            return "Signed up", STATUS_OK
    except ValueError as error:
        return str(error), STATUS_BAD_REQUEST
    except PyMongoError as error:
        return "Server database error: " + str(error), STATUS_BAD_REQUEST


# remove account
@app.route('/api/deactivate', methods=["DELETE"])
def deactivate_user():
    try:
        user = check_google_token()
        if user_exist(user):
            deactivate(user)
            return "Account deactivated", STATUS_OK
        else:
            return "You haven't signed up yet.", STATUS_BAD_REQUEST
    except ValueError as error:
        return str(error), STATUS_BAD_REQUEST
    except PyMongoError as error:
        return "Server database error: " + str(error), STATUS_BAD_REQUEST


# get user info
@app.route('/api/user', methods=["GET"])
def get_user_profile():
    try:
        user = check_google_token()
        if not user_exist(user):
            return wrap_response((STATUS_OK, "Invalid user. Try log in again"))
        else:
            user_info = get_user(user)
            user_info["id"] = user_info["_id"]
            return dumps(user_info), STATUS_OK
    except ValueError as error:
        return str(error), STATUS_BAD_REQUEST
    except PyMongoError as error:
        return "Server database error: " + str(error), STATUS_BAD_REQUEST


# graphql endpoints
app.register_blueprint(graphql_page)

if __name__ == '__main__':
    app.run()
