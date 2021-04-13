from unittest import TestCase
from course_scheduler_server.CIS_API.section import Section


class TestSection(TestCase):
    def test_section_to_dict(self):
        """
        Test Section structure and section_to_dict
        """
        section = Section('1', 1, 1, 1, 1, 1, 1, 1, 1)
        section_dict = section.section_to_dict()
        assert section_dict['section_id'] == 1
        assert section_dict['end_date'] == 1
        assert section_dict['meetings'] == 1
