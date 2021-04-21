import os
from pathlib import Path
from unittest import TestCase
import dotenv
from course_scheduler_server.gpa import parse_course_gpas

dotenv.load_dotenv()


class Test(TestCase):
    parsed_result = parse_course_gpas(str(Path(os.getenv('UCS_PROJECT_ROOT')) / 'gpa-test.csv'))

    def test_first_course(self):
        assert self.parsed_result[0]['course_id'] == 'AAS 100'

    def test_first_course_first_instructor(self):
        assert self.parsed_result[0]['instructor_grades'][0]['first_name'] == 'Simon'
        assert self.parsed_result[0]['instructor_grades'][0]['last_name'] == 'Boonsripaisal'

    def test_first_course_first_instructor_first_term(self):
        assert self.parsed_result[0]['instructor_grades'][0]['term_mean_grades'][0]['year'] == '2020'
        assert self.parsed_result[0]['instructor_grades'][0]['term_mean_grades'][0]['semester'] == 'sp'

    def test_first_course_first_instructor_mean_grades(self):
        grades = self.parsed_result[0]['instructor_grades'][0]['mean_grades']
        assert grades[0] == 8.5
        assert grades[1] == 12
        assert grades[2] == 2.5

    def test_first_course_second_instructor_first_term_grades(self):
        grades = self.parsed_result[0]['instructor_grades'][0]['term_mean_grades'][0]['grades']
        assert grades[0] == 8.5
        assert grades[1] == 12
        assert grades[2] == 2.5

    def test_tenth_course(self):
        assert self.parsed_result[9]['course_id'] == 'ACCY 202'

    def test_tenth_course_third_instructor(self):
        assert self.parsed_result[9]['instructor_grades'][2]['first_name'] == 'Xiongjie'
        assert self.parsed_result[9]['instructor_grades'][2]['last_name'] == 'Li'

    def test_tenth_course_third_instructor_first_term(self):
        assert self.parsed_result[9]['instructor_grades'][2]['term_mean_grades'][0]['year'] == '2020'
        assert self.parsed_result[9]['instructor_grades'][2]['term_mean_grades'][0]['semester'] == 'sp'

    def test_tenth_course_third_instructor_mean_grades(self):
        grades = self.parsed_result[9]['instructor_grades'][2]['mean_grades']
        assert grades[0] == 4.5
        assert grades[1] == 7.5
        assert grades[2] == 1

    def test_tenth_course_third_instructor_first_term_grades(self):
        grades = self.parsed_result[9]['instructor_grades'][2]['term_mean_grades'][0]['grades']
        assert grades[0] == 4.5
        assert grades[1] == 7.5
        assert grades[2] == 1


