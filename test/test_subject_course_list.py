from unittest import TestCase
from CIS_API.subject_course_list import subject_courses_parser


class Test(TestCase):
    def test_invalid_subject_id(self):
        """
        test parse course given invalid subject id
        """
        parsed_response = subject_courses_parser('ass')
        assert parsed_response is False

    def test_invalid_year_semester(self):
        """
        test parse course given valid subject id but invalid year-semester
        """
        parsed_response = subject_courses_parser('AAS', '2/fa')
        assert parsed_response is False

    def test_subject_courses_parser(self):
        """
        test parse course given valid subject and valid year-semester
        """
        parsed_response = subject_courses_parser('AAS', '2020/fall/')
        assert parsed_response['subject_id'] == 'AAS'
        assert list(parsed_response['courses'][0].keys())[0] == '100'
        assert parsed_response['courses'][0]['100'] == 'Intro Asian American Studies'
