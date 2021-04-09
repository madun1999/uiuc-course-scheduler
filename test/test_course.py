from unittest import TestCase
from CIS_API.course import Course, course_parser


class TestCourse(TestCase):
    def test_course_to_dict(self):
        """
        Test Course structure and course_to_dict
        """
        course = Course(1, 'title', 1, 1, 1)
        course_dict = course.course_to_dict()
        assert course_dict['course_id'] == 1
        assert course_dict['title'] == 'title'

    def test_invalid_semester_year(self):
        """
        Test parse a course given invalid semester-year
        """
        parsed_course = course_parser('CS/233', '20/fa')
        assert parsed_course is False

    def test_invalid_course_id(self):
        """
        Test parse a course given valid semester-year but invalid course id
        """
        parsed_course = course_parser('CS/2', '2021/fall/')
        assert parsed_course is False

    def test_course_parser(self):
        """
        Test parse a course given valid semester-year and course id
        """
        parsed_course = course_parser('CS/242', '2018/fall/')
        assert parsed_course['course_id'] == 'CS 242'
        assert parsed_course['title'] == 'Programming Studio'
        assert parsed_course['credit_hours'] == '3 hours.'
        assert len(parsed_course['sections']) == 5
        assert parsed_course['sections'][0]['section_id'] == 45328
        assert parsed_course['sections'][0]['part_of_term'] == '1'
        assert parsed_course['sections'][0]['meetings'][0]['meeting_type'] == 'Laboratory'
        assert parsed_course['sections'][0]['meetings'][0]['instructors'][0]['last_name'] == 'Woodley'