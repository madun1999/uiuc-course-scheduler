from unittest import TestCase
from models.section import Section, make_section


class TestSection(TestCase):
    def test_section_to_dict(self):
        """
        Test Section structure and section_to_dict
        """
        section = make_section(section_id='1',
                               section_number=1,
                               section_title=1,
                               section_text=1,
                               part_of_term=1,
                               enrollment_status=1,
                               start_date=1,
                               end_date=1,
                               meetings=1, )
        assert section['section_id'] == 1
        assert section['end_date'] == 1
        assert section['meetings'] == 1
