"""Scheduler algorithm."""
# Note: "section_id" and "CRN" are equivalent in comments
import time
from typing import List, Tuple, Optional, Set, Callable

from db.gpa_handler import get_section_gpa
from models.course import Course
from scheduler.schedule import Schedule, Factor
from itertools import combinations, chain

TIME_FORMAT = "%I:%M %p"


def get_section_dict(courses):
    """Get dict from section ids to sections for all sections in list of courses"""
    section_dict = {}
    for course in courses:
        for section in course['sections']:
            section_dict[section['section_id']] = section
    return section_dict


def meeting_collides(meetings_a, meetings_b):
    """Determines if section_a and section_b cannot be scheduled together"""
    # check days_of_the_week
    if "days_of_the_week" not in meetings_a or "days_of_the_week" not in meetings_b:
        return False  # no days of the week
    if not meetings_a["days_of_the_week"] or not meetings_b["days_of_the_week"]:
        return False  # no days of the week
    days_a = set(meetings_a["days_of_the_week"].strip())
    days_b = set(meetings_b["days_of_the_week"].strip())
    if not days_a.intersection(days_b):
        return False  # not scheduled on the same day

    # check time of the day
    try:
        start_a = time.strptime(meetings_a["start"], TIME_FORMAT)
        end_a = time.strptime(meetings_a["end"], TIME_FORMAT)
        start_b = time.strptime(meetings_b["start"], TIME_FORMAT)
        end_b = time.strptime(meetings_b["end"], TIME_FORMAT)
    except (ValueError, KeyError) as error:
        return False  # one of the classes does not have time
    return (start_a < end_b) and (start_b < end_a)  # True if conflicted


def section_collides_memoizer(f):
    """Memoize the section collision checker"""
    section_col_memo = {}

    def memoized_section_collides(sec_a, sec_b):
        sec_pair_key = frozenset((sec_a["section_id"], sec_b["section_id"]))  # use set of CRN as keys
        if sec_pair_key not in section_col_memo:
            section_col_memo[sec_pair_key] = f(sec_a, sec_b)
        return section_col_memo[sec_pair_key]

    return memoized_section_collides


@section_collides_memoizer
def section_collides(section_a, section_b):
    """Determines if section_a and section_b cannot be scheduled together"""
    # check part of term
    a_term = section_a["part_of_term"]
    b_term = section_b["part_of_term"]
    if a_term != b_term and a_term != "1" and b_term != "1":  # part_of_term "1" means ALL parts of term
        return False
    # check meeting times
    meetings_a = section_a["meetings"]
    meetings_b = section_b["meetings"]
    for meeting_a in meetings_a:
        for meeting_b in meetings_b:
            if meeting_collides(meeting_a, meeting_b):
                return True
    return False


# https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
def powerset(iterable):
    """Return powerset of iterable. (1,2,3) -> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def fit_course_in_schedules(schedules: Set[Schedule], course) -> Set[Schedule]:
    """
    @deprecated
    Fit a course in schedules. Return list of fitted schedules that contains course.
    """
    new_schedules = set()
    for old_schedule in schedules:  # schedule is Schedule object
        for new_section in course["sections"]:
            # check collision between schedule and new_section
            collision = False
            for old_section in old_schedule.enumerate_sections():
                if section_collides(new_section, old_section):
                    collision = True
                    break
            # if no collision, add the new section to the schedule and save it to new_schedules
            if not collision:
                schedule_copy = old_schedule.copy()
                schedule_copy.add_section(new_section)
                new_schedules.add(schedule_copy)
    return new_schedules


def _schedule_courses_memoizer(f):
    """Memoize _schedule_courses"""
    course_schedule_memo = {}

    def memoized__schedule_courses(courses):
        # use set of course_id as keys
        course_list_key = frozenset([course["course_id"] for course in courses])
        if course_list_key not in course_schedule_memo:
            course_schedule_memo[course_list_key] = f(courses)
        return course_schedule_memo[course_list_key]

    return memoized__schedule_courses


@_schedule_courses_memoizer
def _schedule_courses(courses: List[Course]) -> Set[Schedule]:
    """
    @deprecated
    Helper function for schedule_courses
    resulting schedules is all possible schedules with all of `courses` input.
    :param courses: list of courses to be scheduled
    :return list of set of CRNs
    """
    # algorithm: try adding the last course in the list to all schedules generated by
    #            subsets of list of remaining courses
    all_schedules = {Schedule()}
    if not courses:
        return all_schedules
    last_course: Course = courses[0]
    remaining_courses: List[Course] = courses[:-1]
    for remaining_courses_subset in powerset(remaining_courses):
        # get all schedules for the subset and try to fit last_course in
        subset_schedules: Set[Schedule] = _schedule_courses(remaining_courses_subset)
        subset_and_last_schedules: Set[Schedule] = fit_course_in_schedules(subset_schedules, last_course)
        all_schedules.union(subset_and_last_schedules)
    return all_schedules


def schedule_courses(courses: List[Course]) -> Tuple[Optional[Set[Schedule]], Optional[str]]:
    """
    @deprecated
    Schedule the given courses.
    Current assumption/constraints:
        - len(courses) <= 20
        - len(schedule) <= len(courses)
        - ignore enrollment_status
        - ignore linked sections (no way to find out links)
        - One section per course
        - courses is a dictionary like the one in graphql api,
             which contain sections, which contain meetings
        - section part_of_term, meeting days_of_the_week, meeting start/end are checked
        - section_id will not be -1 (used for breaks)
    :param courses: list of course details
    :return list of list of sections in dictionaries, error string
    """
    if len(courses) > 20:
        return None, "Too many courses"
    schedules: Set[Schedule] = set()
    for courses_subset in powerset(courses):
        schedules.union(_schedule_courses(courses_subset))
        # convert list of set of CRNs to list of list of sections
    return schedules, None  # result, error string


def mean(lst: List[float]) -> float:
    """Average of a list of float. Return 0 for empty lists."""
    if len(lst) == 0:
        return 0
    return sum(lst) / len(lst)


def schedule_score_gen(factors: Factor) -> Callable[[Schedule], float]:
    """
    Generate a scorer for schedules.
    Scores are given as the following:
    100 score for each section in the schedule
    20 score for each section with gpa information
    6 * factor * a_rate score for each section a_rate and take average
    factor * gpa score for each section gpa and take average
    :param factors: Factor to consider
    :return: a scorer of schedules
    """
    gpa_factor = factors["gpa"]
    if gpa_factor is None:
        gpa_factor = 0
    a_rate_factor = factors["aRate"]
    if a_rate_factor is None:
        a_rate_factor = 0

    def schedule_score(schedule: Schedule):
        gpa_infos = [get_section_gpa(section["section_id"]) for section in schedule.enumerate_sections()]
        gpa_infos = list(filter(lambda x: x is not None, gpa_infos))
        # section count score
        section_count_score = schedule.count() * 100
        # has gpa info score
        gpa_present_score = 20 * len(gpa_infos)
        # A rate score and average GPA score
        a_rates = [gpa_info["a_rate"] for gpa_info in gpa_infos]
        gpas = [gpa_info["gpa"] for gpa_info in gpa_infos]
        a_rate_score = 6 * a_rate_factor * mean(a_rates)
        gpa_score = gpa_factor * mean(gpas)
        return section_count_score + gpa_present_score + gpa_score + a_rate_score

    return schedule_score
