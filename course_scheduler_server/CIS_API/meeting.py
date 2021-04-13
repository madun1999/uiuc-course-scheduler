class Meeting:
    """
    Meeting structure
    """
    def __init__(self,
                 meeting_type,
                 start,
                 end,
                 days_of_the_week,
                 building_name,
                 room_number,
                 instructors
                 ):
        """
        Initialization
        :param meeting_type: meeting type (Lecture, Lecture-Discussion, Laboratory, Discussion/Recitation)
        :param start: start time
        :param end: end time
        :param days_of_the_week: days of the week
        :param building_name: building name
        :param room_number: room number
        :param instructors: instructors
        """
        self.meeting_type = meeting_type
        self.start = start
        self.end = end
        if days_of_the_week is not None:
            self.days_of_the_week = days_of_the_week.strip()
        else:
            self.days_of_the_week = None
        self.building_name = building_name
        self.room_number = room_number
        self.instructors = instructors

    def meeting_to_dict(self):
        """
        :return: convert a Meeting object to a dict
        """
        return {
            'meeting_type': self.meeting_type,
            'start': self.start,
            'end': self.end,
            'days_of_the_week': self.days_of_the_week,
            'building_name': self.building_name,
            'room_number': self.room_number,
            'instructors': self.instructors
        }
