class Section:
    """
    Section structure
    """
    def __init__(self,
                 section_id,
                 section_number,
                 section_text,
                 part_of_term,
                 enrollment_status,
                 start_date,
                 end_date,
                 meetings,
                 ):
        """
        Initialization
        :param section_id: section id (CRN)
        :param section_number: section number
        :param section_text: section info
        :param part_of_term: part of term (1, A, B, S1, S2, S2A, S2B, SF)
        :param enrollment_status: enrollment status
        :param start_date: start date
        :param end_date: end date
        :param meetings: a list of meetings
        """
        self.section_id = int(section_id)
        self.section_number = section_number
        self.section_text = section_text
        self.part_of_term = part_of_term
        self.enrollment_status = enrollment_status
        self.start_date = start_date
        self.end_date = end_date
        self.meetings = meetings

    def section_to_dict(self):
        """
        :return: convert a Section object to a dict
        """
        return {
            'section_id': self.section_id,
            'section_number': self.section_number,
            'section_text': self.section_text,
            'part_of_term': self.part_of_term,
            'enrollment_status': self.enrollment_status,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'meetings': self.meetings
        }
