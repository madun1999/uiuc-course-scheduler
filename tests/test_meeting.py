from unittest import TestCase
from models.meeting import Meeting, make_meeting


class TestMeeting(TestCase):
    def test_meeting_to_dict(self):
        """
        Test Meeting structure and meeting_to_dict
        """
        meeting = make_meeting(meeting_type=1,
                               start=1,
                               end=1,
                               days_of_the_week='  MW   ',
                               building_name=1,
                               room_number=1,
                               instructors=1)
        assert meeting['meeting_type'] == 1
        assert meeting['days_of_the_week'] == 'MW'
