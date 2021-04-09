import requests
from xml.etree import ElementTree
from CIS_API.section import Section
from CIS_API.meeting import Meeting
from CIS_API.instructor import Instructor
from db.db_handler import post_course


class Course:
    """
    Course structure
    """
    def __init__(self, course_id, title, description, credit_hours, sections):
        """
        Initialization
        :param course_id: course id
        :param title: course title
        :param description: course description
        :param credit_hours: course credit hour
        :param sections: a list of course sections
        """
        self.course_id = course_id
        self.title = title
        self.description = description
        self.credit_hours = credit_hours
        self.sections = sections

    def course_to_dict(self):
        """
        :return: convert a Course object to a dict
        """
        return {
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'credit_hours': self.credit_hours,
            'sections': self.sections
        }


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


def course_parser(course_id, year_semester='2021/fall/'):
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
    # sections in the course
    sections = []
    for section in course_root.find('detailedSections'):
        # meetings in the section
        meetings = []
        for meeting in section.find('meetings'):
            # instructors in the meeting
            instructors = []
            for instructor in meeting.find('instructors'):
                current_instructor = Instructor(
                    instructor.attrib['firstName'],
                    instructor.attrib['lastName']
                )
                instructors.append(current_instructor.instructor_to_dict())
            current_meeting = Meeting(
                meeting.find('type').text,
                meeting.find('start').text,
                feature_check_exist_and_return(meeting, 'end'),
                feature_check_exist_and_return(meeting, 'daysOfTheWeek'),
                feature_check_exist_and_return(meeting, 'buildingName'),
                feature_check_exist_and_return(meeting, 'roomNumber'),
                instructors
            )
            meetings.append(current_meeting.meeting_to_dict())

        current_section = Section(
            section.attrib['id'],
            section.find('sectionNumber').text,
            feature_check_exist_and_return(section, 'sectionText'),
            section.find('partOfTerm').text,
            section.find('enrollmentStatus').text,
            section.find('startDate').text,
            section.find('endDate').text,
            meetings
        )
        sections.append(current_section.section_to_dict())

    course = Course(
        course_root.attrib['id'],
        course_root.find('label').text,
        course_root.find('description').text,
        course_root.find('creditHours').text,
        sections
    )
    return course.course_to_dict()


def add_course_to_db(course_id, year_semester='2021/fall/'):
    """
    :param course_id: course id, i.e. 'CS/233'
    :param year_semester: year semester, i.e. '2021/fall/'
    :return: add the parsed course into database
    """
    parsed_course = course_parser(course_id, year_semester)
    if parsed_course is not False:
        post_course(parsed_course)


if __name__ == "__main__":
    """
    for testing and demo  
    """
    add_course_to_db('CS/233')
    print(course_parser('CS/233'))
    print(course_parser('CS/3'))
    print(course_parser('CS/233', 'as/a'))
    add_course_to_db('CS/242')
