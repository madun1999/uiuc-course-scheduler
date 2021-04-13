"""API Server"""
from json import dumps
from db.login import deactivate, get_user, sign_up, user_exist
from flask import Flask, request
from flask_cors import CORS
from pymongo.errors import PyMongoError
from google.oauth2 import id_token
from google.auth.transport import requests
from models.user import User
# the app
app = Flask(__name__)
# CORS
CORS(app)
STATUS_OK = 200
STATUS_BAD_REQUEST = 400

CLIENT_IDS = [
    "399183208162-br9tdb9ob4figvn6jr3cds1s60lgpook.apps.googleusercontent.com",
    "399183208162-ms7dgnih1f63lfa4qhe89m6f3ou8d7t4.apps.googleusercontent.com"
]

def wrap_response(result):
    """create response, abort if error"""
    code, response = result
    if code != STATUS_OK:
        return response, code
    else:
        return response

def check_google_token() -> User:
    """Check if the current google token is valid. Return User object if valid. """
    # get token
    auth = request.headers.get("Authorization")
    if not auth:
    	raise ValueError('Invalid Authorization.')
    bearer = auth.split() 
    if bearer[0] != "Bearer":
        raise ValueError('Invalid token type.')
    token = bearer[1]
    # check token
    id_info = id_token.verify_oauth2_token(token, requests.Request())
    if id_info["aud"] not in CLIENT_IDS:
        raise ValueError('Could not verify audience.')
    user_id = id_info['sub']
    user_email = id_info['email']
    return User(user_id, user_email)

# login
@app.route('/api/login', methods=["POST"])
def login_user():
    try:
        user = check_google_token()
        if user_exist(user):
            return wrap_response((STATUS_OK, "Logged in"))
        else:
            sign_up(user)
            return wrap_response((STATUS_OK, "Signed up"))
    except ValueError as error:
        return wrap_response((STATUS_BAD_REQUEST, str(error)))
    except PyMongoError as error:
        return wrap_response((STATUS_BAD_REQUEST, "Server database error: " + str(error)))

# remove account
@app.route('/api/deactivate', methods=["DELETE"])
def deactivate_user():
    try:
        user = check_google_token()
        if user_exist(user):
            deactivate(user)
            return wrap_response((STATUS_OK, "Account deactivated"))
        else:
            return wrap_response((STATUS_BAD_REQUEST, "You haven't signed up yet."))
    except ValueError as error:
        return wrap_response((STATUS_BAD_REQUEST, str(error)))
    except PyMongoError as error:
        return wrap_response((STATUS_BAD_REQUEST, "Server database error: " + str(error)))

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
            return wrap_response((STATUS_OK, dumps(user_info)))
    except ValueError as error:
        return wrap_response((STATUS_BAD_REQUEST, str(error)))
    except PyMongoError as error:
        return wrap_response((STATUS_BAD_REQUEST, "Server database error: " + str(error)))


if __name__ == '__main__':
    app.run()
