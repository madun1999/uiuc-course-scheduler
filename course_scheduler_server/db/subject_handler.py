from db.db_helper import find, replace_one


def post_subject(subject):
    """
    Add a subject to database
    :param subject: the subject to add
    """
    replace_one("subjects", {'subject_id': subject['subject_id']}, subject)


def post_subject_courses(subject_courses):
    """
    Add a subject courses to database
    :param subject_courses: the subject courses to add
    """
    replace_one("subject_courses", {'subject_id': subject_courses['subject_id']}, subject_courses)


def get_all_subjects():
    """Get all subjects from db"""
    all_subjects_obj = find('subjects', {})
    return [subject for subject in all_subjects_obj]