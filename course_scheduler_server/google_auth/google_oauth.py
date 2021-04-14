from flask import request
from google.oauth2 import id_token
from google.auth.transport import requests
from models.user import User

CLIENT_IDS = [
    "399183208162-br9tdb9ob4figvn6jr3cds1s60lgpook.apps.googleusercontent.com",
    "399183208162-ms7dgnih1f63lfa4qhe89m6f3ou8d7t4.apps.googleusercontent.com"
]


def get_from_dict(dictionary, key):
    """get key from dictionary, None if not found"""
    if key not in dictionary:
        return None
    else:
        return dictionary[key]


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
    user_email = get_from_dict(id_info, 'email')
    user_name = get_from_dict(id_info, 'name')
    user_picture = get_from_dict(id_info, 'picture')
    return User(user_id, user_email, user_name, user_picture)
