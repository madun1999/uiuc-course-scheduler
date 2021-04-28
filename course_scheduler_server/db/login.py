"""
A module for communication with the mongo database for user information.
"""

from course_scheduler_server.db.db_helper import delete_one, has_key, replace_one_with_key, set_fields, find_one
from course_scheduler_server.models.user import User, user_to_db_dict


def user_exist(user: User) -> bool:
    """Return if the user exists in the database."""
    return has_key("user", user["id"])


def sign_up(user: User) -> bool:
    """Sign a user up in database"""
    if not has_key("user", user["id"]):
        replace_one_with_key("user", user["id"], user_to_db_dict(user))
        return True
    else:
        return False


def deactivate(user: User) -> bool:
    """Remove a user in database"""
    if has_key("user", user["id"]):
        delete_one("user", {"_id": user["id"]})
        return True
    else:
        return False


def set_user(user: User) -> bool:
    """Set a user's info in database"""
    if not has_key("user", user["id"]):
        return False
    else:
        set_fields("user", user["id"], user_to_db_dict(user))
        return True


def get_user(user: User) -> dict:
    """Get all user info from database"""
    if not has_key("user", user["id"]):
        return {}
    else:
        found_user = find_one("user", {"_id": user["id"]})
        return found_user


def update_user(user: User) -> bool:
    """Update user info to db"""
    if not has_key("user", user["id"]):
        return False
    else:
        found_user = replace_one_with_key("user", user["id"], user_to_db_dict(user))
        return True
