import requests
from xml.etree import ElementTree
from CIS_API.subject_list import subject_parser
from db.db_handler import post_subject_courses


def subject_courses_parser(subject_id, year_semester='2021/fall/'):
    """
    Parse the list of courses given subject id and year-semester
    :param subject_id: subject id, i.e., 'CS/242'
    :param year_semester: year-semester, i.e, '2021/fall/'
    :return: parsed list of courses
    """
    courses_response = requests.get(
        url='https://courses.illinois.edu/cisapp/explorer/schedule/' + year_semester + subject_id + '.xml')
    if courses_response.status_code != 200:
        print("invalid input")
        return False
    courses_root = ElementTree.fromstring(courses_response.content)
    courses = []
    for course in courses_root.find('courses'):
        courses.append({course.attrib['id']: course.text})
    subject_courses = {
        'subject_id': subject_id,
        'courses': courses
    }
    return subject_courses


def add_subject_courses_to_db(subject_id, year_semester='2021/fall/'):
    """
    Add the parsed list of courses given subject id and year-semester into database
    :param subject_id: subject_id: subject id, i.e., 'CS/242'
    :param year_semester: year-semester, i.e, '2021/fall/'
    """
    parsed_courses = subject_courses_parser(subject_id, year_semester)
    if parsed_courses is not False:
        post_subject_courses(parsed_courses)


def add_all_subject_courses_to_db(year_semester='2021/fall/'):
    """
    Add all parsed lists of courses for all subjects given year-semester into database
    :param year_semester: year-semester, i.e, '2021/fall/'
    :return: all parsed list of courses
    """
    subjects = subject_parser(year_semester[:-1])
    if subjects is not False:
        courses = []
        for subject in subjects:
            subject_id = subject['subject_id']
            parsed_courses = subject_courses_parser(subject_id, year_semester)
            if parsed_courses is not False:
                post_subject_courses(parsed_courses)
                courses.append(parsed_courses)
        return courses


if __name__ == "__main__":
    """
    for testing and demo 
    """
    add_all_subject_courses_to_db()
    print(subject_courses_parser('AAS', 'f/2'))
    print(subject_courses_parser('as'))
    print(subject_courses_parser('AAS'))
