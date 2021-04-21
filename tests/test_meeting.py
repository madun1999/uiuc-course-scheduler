from unittest import TestCase
from models.meeting import Meeting, make_meeting


class TestMeeting(TestCase):
    def test_meeting_to_dict(self):
        """
        Test Meeting structure and meeting_to_dict
        """
        meeting = make_meeting(1, 1, 1, '  MW   ', 1, 1, 1)
        assert meeting['meeting_type'] == 1
        assert meeting['days_of_the_week'] == 'MW'
