from flask import request, abort
from werkzeug.exceptions import BadRequest

STATUS_BAD_REQUEST = 400
STATUS_BAD_PAYLOAD = 415
STATUS_OK = 200


def _check_json_payload():
    """check if json payload is valid. Returns payload"""
    if not request.is_json:
        abort(STATUS_BAD_PAYLOAD, "Payload is not json.")
    try:
        payload = request.get_json()
        return payload
    except BadRequest:
        abort(STATUS_BAD_REQUEST, "Data is not valid json.")
