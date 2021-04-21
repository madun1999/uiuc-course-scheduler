from typing import Optional, List, TypedDict
from models.instructor import Instructor


class Meeting(TypedDict):
    """
    Meeting structure
    """
    meeting_type: str
    start: str
    end: Optional[str]
    days_of_the_week: Optional[str]
    building_name: Optional[str]
    room_number: Optional[str]
    instructors: List[Instructor]


def make_meeting(*_,
                 meeting_type,
                 start,
                 end,
                 days_of_the_week,
                 building_name,
                 room_number,
                 instructors) -> Meeting:
    """
    Make a new meeting
    :param meeting_type: meeting type (Lecture, Lecture-Discussion, Laboratory, Discussion/Recitation)
    :param start: start time
    :param end: end time
    :param days_of_the_week: days of the week
    :param building_name: building name
    :param room_number: room number
    :param instructors: instructors
    """
    return Meeting(
        meeting_type=meeting_type,
        start=start,
        end=end,
        days_of_the_week=None if days_of_the_week is None else days_of_the_week.strip(),
        building_name=building_name,
        room_number=room_number,
        instructors=instructors
    )
