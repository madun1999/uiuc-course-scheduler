import requests
from xml.etree import ElementTree
from db.subject_handler import post_subject
from models.subject import make_subject


def fetch_subjects_from_CIS(year_semester='2021/fall'):
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
        current_subject = make_subject(
            subject_id=subject.attrib['id'],
            name=subject.text
        )
        subjects.append(current_subject)
    return subjects


def add_subjects_to_db(year_semester='2021/fall'):
    """
    Add the list of parsed subjects into database
    :param year_semester: year-semester, i.e, '2021/fall'
    """
    subjects = fetch_subjects_from_CIS(year_semester)
    if subjects is not False:
        for subject in subjects:
            post_subject(subject)
    else:
        return False


if __name__ == "__main__":
    """
    for testing and demo 
    """
    add_subjects_to_db()
    fetch_subjects_from_CIS('20/fa')
    print(fetch_subjects_from_CIS())
