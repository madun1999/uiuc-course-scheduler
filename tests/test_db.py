import pymongo
from course_scheduler_server.db.login import deactivate, get_user, sign_up, user_exist
from course_scheduler_server.models.user import User
from os import getenv
from dotenv import load_dotenv

load_dotenv()
mongo_client = pymongo.MongoClient(getenv("MONGODB_CONNECT"))
mongo_db = mongo_client[getenv("MONGODB_DB")]
user_collection = mongo_db["user"]

ID_TOKEN = getenv("TEST_TOKEN")


# db

def test_sign_up(app, client):
    sign_up(User("1", "1@1.com"))
    assert user_exist(User("1", "1@1.com"))
    deactivate(User("1", "1@1.com"))


def test_sign_up_already_exists(app, client):
    sign_up(User("1", "1@1.com"))
    assert not sign_up(User("1", "1@1.com"))


def test_deactivate(app, client):
    sign_up(User("1", "1@1.com"))
    deactivate(User("1", "1@1.com"))
    assert not user_exist(User("1", "1@1.com"))


def test_deactivate_nonexist(app, client):
    deactivate(User("1", "1@1.com"))
    assert not deactivate(User("1", "1@1.com"))


def test_get_user(app, client):
    sign_up(User("1", "1@1.com"))
    user = get_user(User("1", "1@1.com"))
    assert user["email"] == "1@1.com"


def test_get_user_nonexist(app, client):
    deactivate(User("1", "1@1.com"))
    assert get_user(User("1", "1@1.com")) == {}


def test_404(app, client):
    r = client.get("invalid_path")
    assert r.status_code == 404


def test_no_auth_header_deactivate(app, client):
    r = client.delete("api/deactivate")
    assert r.status_code == 400


def test_no_auth_header_login(app, client):
    r = client.post("api/login")
    assert r.status_code == 400


def test_no_auth_header_user(app, client):
    r = client.get("api/user")
    assert r.status_code == 400
