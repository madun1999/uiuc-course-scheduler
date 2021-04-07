"""File with server actions. Return values are all (code, response)"""
from lark.exceptions import UnexpectedInput
from pymongo.errors import PyMongoError
from bookscraper.database import query_parser
from bson.json_util import dumps
from argparse import Namespace
from bookscraper.database import db_tools
from bookscraper.tools import validate_args
from bookscraper.scraper.scraper import CrawlingService


def normalize_id(payload):
    """Add _id to payload if not present"""
    if "book_id" in payload:
        payload["_id"] = payload["book_id"]
    if "author_id" in payload:
        payload["_id"] = payload["author_id"]
    return payload


def do_post_one(collection, use_payload):
    """POST one"""
    try:
        use_payload = normalize_id(use_payload)
        db_tools.replace_one_with_key(collection, use_payload["_id"], use_payload)
    except (PyMongoError, TypeError, KeyError):
        return 400, "Error posting to " + collection
    return 200, "Successfully posted to " + collection


def do_post_many(collection, use_payload):
    """POST many"""
    for payload_item in use_payload:
        try:
            payload_item = normalize_id(payload_item)
            db_tools.replace_one_with_key(collection, payload_item["_id"], payload_item)
        except (PyMongoError, TypeError, KeyError):
            return 400, "Error posting to " + collection
    return 200, "Successfully posted to " + collection


def do_post(collection, use_payload):
    """POST request, calls do_post_one or do_post_many"""
    if collection.endswith("s"):
        return do_post_many(collection, use_payload)
    else:
        return do_post_one(collection + "s", use_payload)


def do_scrape(use_scrape_info):
    """
    Scrape request
    use_scrape_info is the representation of the dict : {"max_books": 1, "max_authors": 1,
    "start_url": "https://www.goodreads.com/book/show/3735293-clean-code"}
    """
    default_info = {"max_books": 1, "max_authors": 1,
                    "start_url": "https://www.goodreads.com/book/show/3735293-clean-code",
                    "verbose": False, "import_json": None}
    default_info.update(use_scrape_info)
    opts = Namespace(**default_info)
    validate_args(opts)
    service = CrawlingService(opts)
    service.crawl()
    return 200, "Crawling Success"


def do_delete(collection, use_id):
    """DELETE request"""
    try:
        db_tools.delete_one(collection, {"_id": use_id})
    except PyMongoError:
        return 400, f"Error deleting id {use_id} from collection {collection}"
    return 200, f"Successfully deleted id {use_id} from collection {collection}"


def do_put(collection, use_id, use_payload):
    """PUT request"""
    try:
        use_payload["_id"] = use_id
        db_tools.set_fields(collection, use_id, use_payload)
    except (PyMongoError, TypeError, KeyError):
        return 400, f"Error updating data at id {use_id} in collection {collection}"
    return 200, f"Successfully updated data at id {use_id} in collection {collection}"


def do_query(use_query):
    """Query request"""
    try:
        query = query_parser.parse_query(use_query)
    except UnexpectedInput:
        return 400, f"Bad query string: {use_query}."
    try:
        items = query.perform_find_query()
    except PyMongoError:
        return 400, "Error performing query."

    items_string = dumps(items)
    return 200, items_string


def do_get(collection, use_id):
    """GET request"""
    try:
        items = list(db_tools.find(collection, {"_id": use_id}))
    except PyMongoError:
        return 400, f"Error getting data with id {use_id} from collection {collection}"
    return 200, dumps(items)

