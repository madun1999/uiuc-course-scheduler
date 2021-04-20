from unittest import TestCase
from course_scheduler_server.CIS_API.instructor import Instructor


class TestInstructor(TestCase):

    def test_instructor_to_dict(self):
        """
        Test Instructor structure and instructor_to_dict
        """
        instructor = Instructor('first', 'last')
        instructor_dict = instructor.instructor_to_dict()
        assert instructor_dict['first_name'] == 'first'
        assert instructor_dict['last_name'] == 'last'
