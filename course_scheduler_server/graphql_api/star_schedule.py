from ariadne import ObjectType, convert_kwargs_to_snake_case
from db.login import get_user, update_user

mutation = ObjectType("Mutation")

star_schedule_binds = [mutation]


@convert_kwargs_to_snake_case
@mutation.field("starSchedule")
def star_schedule(_, info, section_ids):
    """
    Sections is a list of SectionIds / CRNs (int)
    """
    cur_user = info.context["cur_user"]
    user = get_user(cur_user)
    user["id"] = user["_id"]
    if "stared_schedule_ids" not in user:
        user["stared_schedule_ids"] = []
    user["stared_schedule_ids"].append(section_ids)
    update_user(user)
    return {"success": True}
