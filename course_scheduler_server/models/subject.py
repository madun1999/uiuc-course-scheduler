from meeting import Meeting
from typing import Optional, List, TypedDict


class Subject(TypedDict):
    subject_id: str
    name: str


def make_subject(*_,
                 subject_id,
                 name,
                 ):
    """
    Make a Subject dict
    :param subject_id: subject short name. e.g. AAS, MATH
    :param name: subject full name. e.g. Asian American Studies
    """
    Subject(
        subject_id=subject_id.strip(),
        name=name.strip()
    )


def verify_subject(obj):
    """Convert a dict to a Subject dict. With data cleaning."""
    return make_subject(subject_id=obj['subject_id'], name=obj['name'])
