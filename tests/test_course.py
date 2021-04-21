from unittest import TestCase
from models.course import Course, make_course
from CIS_API.fetch_course import fetch_course_from_CIS


class TestCourse(TestCase):
    def test_course_to_dict(self):
        """
        Test Course structure and course_to_dict
        """
        course = make_course(course_id=1, title='title', credit_hours=1, description=1, sections=1)
        assert course['course_id'] == 1
        assert course['title'] == 'title'

    def test_invalid_semester_year(self):
        """
        Test parse a course given invalid semester-year
        """
        parsed_course = fetch_course_from_CIS('CS/233', '20/fa')
        assert parsed_course is False

    def test_invalid_course_id(self):
        """
        Test parse a course given valid semester-year but invalid course id
        """
        parsed_course = fetch_course_from_CIS('CS/2', '2021/fall/')
        assert parsed_course is False

    def test_course_parser(self):
        """
        Test parse a course given valid semester-year and course id
        """
        parsed_course = fetch_course_from_CIS('CS/242', '2018/fall/')
        assert parsed_course['course_id'] == 'CS 242'
        assert parsed_course['title'] == 'Programming Studio'
        assert parsed_course['credit_hours'] == '3 hours.'
        assert len(parsed_course['sections']) == 5
        assert parsed_course['sections'][0]['section_id'] == 45328
        assert parsed_course['sections'][0]['part_of_term'] == '1'
        assert parsed_course['sections'][0]['meetings'][0]['meeting_type'] == 'Laboratory'
        assert parsed_course['sections'][0]['meetings'][0]['instructors'][0]['last_name'] == 'Woodley'