from meeting import Meeting
from typing import Optional, List


class Subject:
    subject_id: str
    name: str
    """
    Section structure
    """

    def __init__(self,
                 subject_id,
                 name,
                 ):
        """
        Initialization
        :param subject_id: subject short name. e.g. AAS, MATH
        :param name: subject full name. e.g. Asian American Studies
        """
        self.subject_id = subject_id.strip()
        self.name = name.strip()

    def subject_to_dict(self):
        """
        :return: convert a Subject object to a dict
        """
        return {
            'subject_id': self.subject_id,
            'name': self.name,
        }

    @classmethod
    def from_dict(cls, obj):
        """convert a dict to a subject object"""
        return Subject(obj['subject_id'], obj['name'])
