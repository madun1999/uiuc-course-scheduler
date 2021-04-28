from models.meeting import Meeting, TypedDict
from typing import Optional, List


class Section(TypedDict):
    section_id: int
    section_number: str
    section_title: Optional[str]
    section_text: Optional[str]
    part_of_term: str
    enrollment_status: str
    start_date: Optional[str]
    end_date: Optional[str]
    meetings: List[Meeting]


def make_section(*_,
                 section_id,
                 section_number,
                 section_title,
                 section_text,
                 part_of_term,
                 enrollment_status,
                 start_date,
                 end_date,
                 meetings,
                 ) -> Section:
    """
    Make a Section dictionary
    :param section_id: section id (CRN)
    :param section_number: section number
    :param section_title: section title
    :param section_text: section info
    :param part_of_term: part of term (1, A, B, S1, S2, S2A, S2B, SF)
    :param enrollment_status: enrollment status
    :param start_date: start date
    :param end_date: end date
    :param meetings: a list of meetings
    """
    return Section(
        section_id=int(section_id),
        section_number=section_number,
        section_title=section_title,
        section_text=section_text,
        part_of_term=part_of_term,
        enrollment_status=enrollment_status,
        start_date=start_date,
        end_date=end_date,
        meetings=meetings,
    )
