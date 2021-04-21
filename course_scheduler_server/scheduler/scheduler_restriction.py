from typing import List, Tuple, Optional, Set

from models.course import make_course
from models.meeting import make_meeting
from models.section import make_section, Section
from scheduler.schedule import AnnotatedCourse, Break, Schedule, make_annotated_section
from scheduler.scheduler import powerset, section_collides


def fit_course_in_schedules(schedules: Set[Schedule], annotated_course: AnnotatedCourse) -> Set[Schedule]:
    """Fit a course in schedules. Return list of fitted schedules that contains course."""
    course = annotated_course["course"]
    mandatory = annotated_course["mandatory"]
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
                schedule_copy.add_section(make_annotated_section(new_section, mandatory))
                new_schedules.add(schedule_copy)
    return new_schedules


def _schedule_courses_memoizer(f):
    """Memoize _schedule_courses"""
    course_schedule_memo = {}

    def memoized__schedule_courses(self, courses: List[AnnotatedCourse]):
        course_list_key = frozenset([course["course"]["course_id"] for course in courses])
        if course_list_key not in course_schedule_memo:
            course_schedule_memo[course_list_key] = f(self, courses)
        return course_schedule_memo[course_list_key]

    return memoized__schedule_courses


class RestrictionScheduler:
    max_courses: int
    min_mandatory: int
    breaks: List[Break]
    break_sections: Schedule  # schedule with virtual sections used to enforce break restriction, copy to use

    def __init__(self,
                 max_courses: int,
                 min_mandatory: int,
                 breaks: List[Break]):
        """
        Scheduler, Initialize with restrictions.
        :param max_courses: Restriction, maximum number of courses in a schedule.
        :param min_mandatory: Restriction, minimum number of mandatory courses in a schedule.
        :param breaks: Restriction, time where you don't want to schedule a class.
        """
        self.max_courses = max_courses
        self.min_mandatory = min_mandatory
        self.breaks = breaks
        self.break_sections = Schedule()
        for idx, break_time in enumerate(breaks):
            meeting = make_meeting(
                meeting_type="LEC",
                start=break_time["start"],
                end=break_time["end"],
                days_of_the_week=break_time["days_of_the_week"],
                building_name="",
                room_number="",
                instructors=[]
            )
            break_sections = make_section(
                section_id=-idx-1,
                section_number=f"BREAK{idx+1}",
                section_title=f"Break{idx+1}",
                section_text="",
                part_of_term="1",
                enrollment_status="Open",
                start_date="",
                end_date="",
                meetings=[meeting],
            )
            self.break_sections.add_section(make_annotated_section(break_sections, False))

    def schedule_courses(
            self,
            courses: List[AnnotatedCourse],
    ) -> Tuple[Optional[Set[Schedule]], Optional[str]]:
        """
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
            - section_id will not be negative (used for breaks)

        :param courses: list of AnnotatedCourse
        :return set of Schedules
        """
        if len(courses) > 20:
            return None, "Too many courses"
        schedules: Set[Schedule] = set()
        for courses_subset in powerset(courses):
            schedules = schedules.union(self._schedule_courses(courses_subset))
        # enforce min mandatory course count
        schedules = {schedule for schedule in schedules if schedule.mandatory_count() >= self.min_mandatory}
        return schedules, None  # result, error string

    @_schedule_courses_memoizer
    def _schedule_courses(self, courses: List[AnnotatedCourse]) -> Set[Schedule]:
        """
        Helper function for schedule_courses
        resulting schedules is all possible schedules with all of `courses` input.
        :param courses: list of courses to be scheduled
        :return list of set of CRNs
        """
        # algorithm: try adding the last course in the list to all schedules generated by
        #            subsets of list of remaining courses
        all_schedules = {self.break_sections.copy()}  # enforce break restriction0
        if not courses:
            return all_schedules
        last_course: AnnotatedCourse = courses[0]
        remaining_courses: List[AnnotatedCourse] = courses[:-1]
        for remaining_courses_subset in powerset(remaining_courses):
            # get all schedules for the subset and try to fit last_course in
            if len(remaining_courses) > self.max_courses:   # enforce max courses restriction
                continue
            subset_schedules: Set[Schedule] = self._schedule_courses(remaining_courses_subset)
            if len(remaining_courses) + 1 <= self.max_courses:  # enforce max courses restriction
                fitted_schedules: Set[Schedule] = fit_course_in_schedules(subset_schedules, last_course)
            else:
                fitted_schedules: Set[Schedule] = subset_schedules
            all_schedules = all_schedules.union(fitted_schedules)
        return all_schedules




