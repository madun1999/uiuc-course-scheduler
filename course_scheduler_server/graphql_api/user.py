import db.section_handler
from db.login import get_user, update_user
import db.course_handler as database
from ariadne import ObjectType


query = ObjectType("Query")
user_query = ObjectType("User")
mutation = ObjectType("Mutation")

user_binds = [query, user_query, mutation]


@query.field("user")
def user_resolver(_, info):
    """Query current user information."""
    cur_user = info.context["cur_user"]
    user = get_user(cur_user)
    user["id"] = user["_id"]
    return user


@user_query.field("staredSchedules")
def user_stared_schedules_resolver(obj, _):
    stared_schedules = obj["stared_schedule_ids"]
    stared_schedules = [[db.section_handler.get_section(section) for section in schedule]
                        for schedule in stared_schedules]
    return stared_schedules


@mutation.field("updateUser")
def update_user_resolver(_, info):
    """Update current user information with current google token."""
    cur_user = info.context["cur_user"]
    update_user(cur_user)
    return {"success": True}
