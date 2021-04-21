from typing import TypedDict, Dict
from typing import Set

from models.course import Course
from models.section import Section


class AnnotatedSection(TypedDict):
    """
    Dictionary containing the section and if it is from a mandatory course
    Used for scheduling with minimum mandatory restrictions.
    """
    section: Section
    section_id: int
    mandatory: bool


def make_annotated_section(section: Section, mandatory: bool):
    return {
        "section": section,
        "section_id": section["section_id"],
        "mandatory": mandatory,
    }


class Schedule:
    """Schedule object for schedule algorithm. Contains set of sections scheduled"""

    def __init__(self):
        self.sections: Dict[int, AnnotatedSection] = dict()

    def add_section(self, section: AnnotatedSection):
        """Add a new annotated section to the schedule"""
        self.sections[section["section_id"]] = section

    def __hash__(self):
        hash(frozenset(self.sections.keys()))

    def __eq__(self, other):
        return frozenset(self.sections.keys()) == frozenset(other.sections.keys())

    def copy(self) -> 'Schedule':
        """shallow copy of the schedule"""
        new_schedule = Schedule()
        new_schedule.sections = self.sections.copy()
        return new_schedule

    def enumerate_sections(self):
        """Returns an iterator for the sections in this schedule. NOT annotated sections."""
        for _, annotated_section in self.sections.values():
            yield annotated_section["section"]

    def mandatory_count(self):
        """Count the number of mandatory sections in this schedule"""
        count = 0
        for _, annotated_section in self.sections.values():
            if annotated_section["mandatory"]:
                count += 1
        return count


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
