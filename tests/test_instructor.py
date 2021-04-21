from unittest import TestCase
from models.instructor import Instructor


class TestInstructor(TestCase):

    def test_instructor_to_dict(self):
        """
        Test Instructor structure and instructor_to_dict
        """
        instructor = Instructor(first_name='first', last_name='last')
        assert instructor['first_name'] == 'first'
        assert instructor['last_name'] == 'last'
