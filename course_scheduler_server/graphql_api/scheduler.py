from ariadne import QueryType
import db.db_CIS_API_handler as database
from scheduler.scheduler_restriction import RestrictionScheduler

query = QueryType()
scheduler_binds = [query]


@query.field("schedule")
def schedule_resolver(*_, courses, restrictions, factors):
    """
    courses is a list of  {"courseId": str, "mandatory": bool}
    restrictions is {"maxCourses": int, "minMandatory": int, breaks: [Break!]}
    where Break is {"start": str, "end": str, "days_of_the_week": str}
    factors is {"gpa": float, "a_rate": float}
    """
    course_details = []
    max_courses = 100 if restrictions["maxCourses"] is None else restrictions["maxCourses"]
    min_mandatory = 0 if restrictions["minMandatory"] is None else restrictions["minMandatory"]
    breaks = [{"start": break1["start"], "end": break1["end"], "days_of_the_week": break1["daysOfTheWeek"]}
              for break1 in restrictions["breaks"]]

    for annotated_course in courses:
        course_id = annotated_course["courseId"]
        mandatory = annotated_course["mandatory"]
        subject = course_id.split()[0]
        course_num = course_id.split()[1]
        course_detail = database.get_course_detail(subject, course_num)
        if not course_detail:
            return {
                "success": False,
                "error": f"Course {course_id} does not exist."
            }
        course_details.append({"course": course_detail, "mandatory": mandatory})
    restriction_scheduler = RestrictionScheduler(max_courses, min_mandatory, breaks)
    schedules, error = restriction_scheduler.schedule_courses(course_details)
    if error:
        return {
            "success": False,
            "error": error
        }
    result = {
        "success": True,
        "schedules": [
            {"sections": schedule.to_list()} for schedule in schedules
        ]
    }
    return result
