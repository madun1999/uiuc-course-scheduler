from xml.etree import ElementTree

import requests

from models.course import Course, make_course
from models.instructor import Instructor
from models.meeting import Meeting, make_meeting
from models.section import Section, make_section


def feature_check_exist_and_return(root, feature):
    """
    :param root: the XML root
    :param feature: feature tag to search for
    :return: None if no such feature tag, text of the feature tag otherwise
    """
    if root.find(feature) is None:
        return None
    else:
        return root.find(feature).text


def instructor_parser(meeting_root):
    """
    Parse instructors in the section
    :param meeting_root: the meeting root
    :return: a list of parsed instructors
    """
    instructors = []
    for instructor in meeting_root.find('instructors'):
        current_instructor = Instructor(
            first_name=instructor.attrib['firstName'],
            last_name=instructor.attrib['lastName']
        )
        instructors.append(current_instructor)
    return instructors


def meeting_parser(section_root):
    """
    Parse meetings in the section
    :param section_root: the section root
    :return: a list of parsed meetings
    """
    meetings = []
    for meeting in section_root.find('meetings'):
        current_meeting: Meeting = make_meeting(
            meeting_type=meeting.find('type').text,
            start=meeting.find('start').text,
            end=feature_check_exist_and_return(meeting, 'end'),
            days_of_the_week=feature_check_exist_and_return(meeting, 'daysOfTheWeek'),
            building_name=feature_check_exist_and_return(meeting, 'buildingName'),
            room_number=feature_check_exist_and_return(meeting, 'roomNumber'),
            instructors=instructor_parser(meeting)
        )
        meetings.append(current_meeting)
    return meetings


def section_parser(course_root):
    """
    Parse sections in the course
    :param course_root: the course root
    :return: a list of parsed sections
    """
    sections = []
    for section in course_root.find('detailedSections'):
        current_section: Section = make_section(
            section_id=section.attrib['id'],
            section_number=section.find('sectionNumber').text,
            section_title=feature_check_exist_and_return(section, 'sectionTitle'),
            section_text=feature_check_exist_and_return(section, 'sectionText'),
            part_of_term=section.find('partOfTerm').text,
            enrollment_status=section.find('enrollmentStatus').text,
            start_date=section.find('startDate').text,
            end_date=section.find('endDate').text,
            meetings=meeting_parser(section)
        )
        sections.append(current_section)
    return sections


def fetch_course_from_CIS(course_id, year_semester='2021/fall/'):
    """
    :param course_id: course id, i.e. 'CS/233'
    :param year_semester: year semester, i.e. '2021/fall/'
    :return: parsed course info as a dict
    """
    course_response = requests.get(
        url='https://courses.illinois.edu/cisapp/explorer/schedule/' + year_semester + course_id + '.xml?mode=detail')
    if course_response.status_code != 200:
        print("invalid input")
        return False
    course_root = ElementTree.fromstring(course_response.content)
    course = make_course(
        course_id=course_root.attrib['id'],
        title=course_root.find('label').text,
        description=course_root.find('description').text,
        credit_hours=course_root.find('creditHours').text,
        sections=section_parser(course_root)
    )
    return course


if __name__ == "__main__":
    """
    for testing and demo  
    """
    print(fetch_course_from_CIS('CS/233'))
    print(fetch_course_from_CIS('CS/3'))
    print(fetch_course_from_CIS('CS/233', 'as/a'))
