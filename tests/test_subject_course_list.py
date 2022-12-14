from unittest import TestCase
from course_scheduler_server.CIS_API.subject_course_list import fetch_subject_courses_from_CIS


class Test(TestCase):
    def test_invalid_subject_id(self):
        """
        test parse course given invalid subject id
        """
        parsed_response = fetch_subject_courses_from_CIS('ass')
        assert parsed_response is False

    def test_invalid_year_semester(self):
        """
        test parse course given valid subject id but invalid year-semester
        """
        parsed_response = fetch_subject_courses_from_CIS('AAS', '2/fa')
        assert parsed_response is False

    def test_subject_courses_parser(self):
        """
        test parse course given valid subject and valid year-semester
        """
        parsed_response = fetch_subject_courses_from_CIS('AAS', '2020/fall/')
        assert parsed_response['subject_id'] == 'AAS'
        assert list(parsed_response['courses'][0].values())[0] == '100'
        assert parsed_response['courses'][0]['title'] == 'Intro Asian American Studies'
