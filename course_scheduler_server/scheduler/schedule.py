from typing import TypedDict, Dict
from typing import Set

from models.course import Course
from models.section import Section


class Schedule:
    """Schedule object for schedule algorithm. Contains set of sections scheduled"""

    def __init__(self):
        self.sections: Dict[int, Section] = dict()

    def add_section(self, section: Section):
        self.sections[section["section_id"]] = section

    def __hash__(self):
        hash(frozenset(self.sections.keys()))

    def __eq__(self, other):
        return frozenset(self.sections.keys()) == frozenset(other.sections.keys())

    def copy(self) -> 'Schedule':
        new_schedule = Schedule()
        new_schedule.sections = self.sections.copy()
        return new_schedule

    def enumerate_sections(self):
        for _, section in self.sections.values():
            yield section


class AnnotatedCourse(TypedDict):
    """
    Dictionary containing the course and if it is mandatory
    Used for scheduling with minimum mandatory restrictions.
    """
    course: Course
    mandatory: bool


class Break(TypedDict):
    """
    Dictionary of a break. Used for scheduling with break restriction.
    """
    start: str
    end: str
    days_of_the_week: str
