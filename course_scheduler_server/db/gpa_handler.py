from functools import lru_cache
from typing import Optional
from db.course_handler import get_course_from_section
from db.db_helper import find_one, replace_one
from db.section_handler import post_section, get_section
from models.GPA import GPA, calculate_gpa


NO_GPA_SECTION = "No GPA info"


def post_course_gpas(course):
    """
    Add course gpas to course_gpas collection
    :param course: the course gpas to add
    """
    replace_one("course_gpas", {'course_id': course['course_id']}, course)


def post_section_gpa(section, gpa):
    """
    Add course gpas to sections collection to the corresponding section
    """
    section["gpa"] = gpa
    post_section(section)


def get_gpa_from_course_gpa(section_id, section) -> Optional[GPA]:
    """Get gpa by section_id from course_gpas collection."""

    course = get_course_from_section(section_id)
    if course is None:
        return None
    course_id = course["course_id"]
    instructors = section["meetings"][0]["instructors"]
    if not instructors:
        return None
    first_name_initial = instructors[0]["first_name"][0].upper()
    last_name = instructors[0]["last_name"]
    gpa_detail = find_one("course_gpas", {"course_id": course_id})
    if not gpa_detail:
        return None
    instructors_gpa = gpa_detail["instructor_grades"]

    def match_name(info):
        return info["first_name"][0].upper() == first_name_initial \
               and info["last_name"] == last_name
    mean_grades_it = filter(match_name, instructors_gpa)
    try:
        mean_grades = next(mean_grades_it)["mean_grades"]
    except StopIteration:  # no instructor found
        return None
    return calculate_gpa(mean_grades)


@lru_cache
def get_section_gpa(section_id: int) -> Optional[GPA]:
    """Get gpa by section_id from sections collection. Add to sections collection if not exist"""
    section = find_one('sections', {'section_id': section_id})
    if section is None:
        section = get_section(section_id)
        if section is None:
            return None
    if "gpa" not in section or section["gpa"] is None:
        gpa = get_gpa_from_course_gpa(section_id, section)
        if gpa is None:
            section["gpa"] = NO_GPA_SECTION
            post_section(section)
            return None
        else:
            post_section_gpa(section, gpa)
    else:
        gpa = section["gpa"]
    if gpa == NO_GPA_SECTION:
        return None
    return gpa


if __name__ == '__main__':
    print(get_section_gpa(64513))
