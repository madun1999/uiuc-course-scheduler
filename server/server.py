"""API Server"""
from flask import Flask, request, abort
from flask_cors import CORS
from multiprocessing import Process
from werkzeug.exceptions import BadRequest
from bookscraper.server import server_actions
from bookscraper.database import db_tools
from bookscraper.tools import standardize_collection_name

app = Flask(__name__)
CORS(app)

def wrap_response(result):
    """create response, abort if error"""
    code, response = result
    if code != 200:
        return response, code
    else:
        return response


def _check_id(collection):
    """check if id is valid and exists in the database"""
    if "id" not in request.args:
        return 400, abort(400, "No id provided.")
    if not request.args["id"].isdigit():
        return 400, abort(400, "Provided id is not int.")
    use_id = int(request.args["id"])
    collection = standardize_collection_name(collection)
    if len(db_tools.find(collection, {"_id": use_id})) == 0:
        return 400, abort(400, f"No id {use_id} in collection " + collection)
    return use_id, None


def _check_json_payload():
    """check if json payload is valid"""
    if not request.is_json:
        return 415, abort(415, "Payload is not json.")
    try:
        payload = request.get_json()
    except BadRequest:
        return 400, abort(400, "Data is not valid json.")
    return payload, None


def _check_collection(collection, standardize=True):
    """check if collection is valid, standardize if needed"""
    if collection not in ["author", "authors", "book", "books"]:
        return 404, abort(404, "Unknown path.")
    if standardize:
        collection = standardize_collection_name(collection)
    return collection, None


@app.route('/api/<collection>', methods=['GET'])
def get_route(collection):
    """GET requests"""
    if collection == "search":
        if "q" not in request.args:
            return 400, abort(400, "No query provided.")
        query = request.args["q"]

        return wrap_response(server_actions.do_query(query))
    else:
        collection, error = _check_collection(collection)
        if error:
            return error
        use_id, error = _check_id(collection)
        if error:
            return error
        return wrap_response(server_actions.do_get(collection, use_id))


@app.route('/api/<collection>', methods=['PUT'])
def put_route(collection):
    """PUT requests"""
    collection, error = _check_collection(collection)
    if error:
        return error
    use_id, error = _check_id(collection)
    if error:
        return error
    payload, error = _check_json_payload()
    if error:
        return error
    return wrap_response(server_actions.do_put(collection, use_id, payload))


@app.route('/api/<collection>', methods=['POST'])
def post_route(collection):
    """POST requests"""
    payload, error = _check_json_payload()
    if error:
        return error
    if collection == "scrape":
        p = Process(target=server_actions.do_scrape, args=(request.json,))
        p.start()
        p.join()
        if p.exitcode != 0:
            return abort(400, "Scraping Failed, check scraping arguments")
        return "Scraping Success"
    else:
        collection, error = _check_collection(collection, standardize=False)
        if error:
            return error
        return wrap_response(server_actions.do_post(collection, payload))


@app.route('/api/<collection>', methods=['DELETE'])
def delete_route(collection):
    """DELETE requests"""
    collection, error = _check_collection(collection)
    if error:
        return error
    use_id, error = _check_id(collection)
    if error:
        return error
    return wrap_response(server_actions.do_delete(collection, use_id))


if __name__ == '__main__':
    app.run()
