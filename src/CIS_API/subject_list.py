import requests
from xml.etree import ElementTree
from db.db_handler import post_subject


def subject_parser(year_semester='2021/fall'):
    """
    Parse all subjects given year-semester
    :param year_semester: year-semester, i.e, '2021/fall'
    :return: parsed list of subject
    """
    subject_response = requests.get(
        url='https://courses.illinois.edu/cisapp/explorer/schedule/' + year_semester + '.xml')
    if subject_response.status_code != 200:
        print("invalid input")
        return False
    subject_root = ElementTree.fromstring(subject_response.content)
    subjects = []
    for subject in subject_root.find('subjects'):
        current_subject = {
            'subject_id': subject.attrib['id'],
            'name': subject.text
        }
        subjects.append(current_subject)
    return subjects


def add_subjects_to_db(year_semester='2021/fall'):
    """
    Add the list of parsed subjects into database
    :param year_semester: year-semester, i.e, '2021/fall'
    """
    subjects = subject_parser(year_semester)
    if subjects is not False:
        for subject in subjects:
            post_subject(subject)


if __name__ == "__main__":
    """
    for testing and demo 
    """
    add_subjects_to_db()
    subject_parser('20/fa')
    print(subject_parser())
