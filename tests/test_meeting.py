from unittest import TestCase
from CIS_API.meeting import Meeting


class TestMeeting(TestCase):
    def test_meeting_to_dict(self):
        """
        Test Meeting structure and meeting_to_dict
        """
        meeting = Meeting(1, 1, 1, '  MW   ', 1, 1, 1)
        meeting_dict = meeting.meeting_to_dict()
        assert meeting_dict['meeting_type'] == 1
        assert meeting_dict['days_of_the_week'] == 'MW'
