from typing import List, TypedDict

from models.section import Section


class Course(TypedDict):
    """
    Course structure
    """
    course_id: str
    title: str
    description: str
    credit_hours: str
    sections: List[Section]


def make_course(*_, course_id, title, description, credit_hours, sections) -> Course:
    """
    Initialization
    :param course_id: course id
    :param title: course title
    :param description: course description
    :param credit_hours: course credit hour
    :param sections: a list of course sections
    """
    return Course(
        course_id=course_id,
        title=title,
        description=description,
        credit_hours=credit_hours,
        sections=sections
    )


class SubjectCourse(TypedDict):
    """
    A simplified version of course used in subject_course collection
    """
    course_num: str
    title: str


def make_subject_course(*_, course_num, title) -> SubjectCourse:
    """
    Initialization
    :param course_num: course number e.g. 233
    :param title: course title
    """
    return SubjectCourse(
        course_num=course_num,
        title=title,
    )
