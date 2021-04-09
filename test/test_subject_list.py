from unittest import TestCase
from CIS_API.subject_list import subject_parser


class Test(TestCase):
    def test_invalid_year_semester(self):
        """
        test subject parser given invalid year-semester
        """
        parsed_subjects = subject_parser('19/fa')
        assert parsed_subjects is False

    def test_subject_parser(self):
        """
        test subject parser given valid year-semester
        """
        parsed_subjects = subject_parser('2020/fall')
        assert parsed_subjects[0]['subject_id'] == 'AAS'
        assert parsed_subjects[0]['name'] == 'Asian American Studies'
        assert parsed_subjects[-1]['subject_id'] == 'YDSH'
        assert parsed_subjects[-1]['name'] == 'Yiddish'