from course_scheduler_server.scheduler import scheduler

# constants for testing
# meeting A collide with B
MEETING_A = {
        "start": "02:00 PM",
        "end": "04:00 PM",
        "days_of_the_week": "MTWRF"
    }
MEETING_B = {
        "start": "03:00 PM",
        "end": "04:00 PM",
        "days_of_the_week": "M"
    }
MEETING_C = {
        "start": "04:00 PM",
        "end": "05:00 PM",
        "days_of_the_week": "M"
    }
MEETING_D = {
        "start": "04:00 PM",
        "end": "05:00 PM",
        "days_of_the_week": "T"
    }

SECTION_A = {
    "section_id": "10086",
    "part_of_term": "1",
    "meetings": [MEETING_A]
}
SECTION_B = {
    "section_id": "12580",
    "part_of_term": "1",
    "meetings": [MEETING_B]
}
SECTION_C = {
    "section_id": "10001",
    "part_of_term": "1",
    "meetings": [MEETING_C]
}
SECTION_C2 = {
    "section_id": "10001",
    "part_of_term": "A",
    "meetings": [MEETING_C]
}
SECTION_A2 = {
    "section_id": "10087",
    "part_of_term": "1",
    "meetings": [MEETING_A]
}
SECTION_B2 = {
    "section_id": "12581",
    "part_of_term": "1",
    "meetings": [MEETING_B]
}
SECTION_DICT = {
    "12580": SECTION_B,
    "10001": SECTION_C,
    "10086": SECTION_A,
}
SCHEDULE_A_LIST = [
    "12580",
    "10001"
]

COURSE_A = {
    "course_id": "CHOC123",
    "sections": [SECTION_A, SECTION_B]
}

COURSE_B = {
    "course_id": "BOX100",
    "sections": [SECTION_A2, SECTION_B2]
}

def test_meeting_collides():
    assert scheduler.meeting_collides(MEETING_A, MEETING_B)

def test_meeting_not_collide():
    assert not scheduler.meeting_collides(MEETING_A, MEETING_C)

def test_meeting_not_collide2():
    assert not scheduler.meeting_collides(MEETING_B, MEETING_C)

def test_meeting_not_collide_day():
    assert not scheduler.meeting_collides(MEETING_C, MEETING_D)

def test_section_collides():
    assert scheduler.section_collides(SECTION_A, SECTION_B)

def test_section_not_collides():
    assert not scheduler.section_collides(SECTION_A, SECTION_C)

def test_section_not_collides_term():
    assert not scheduler.section_collides(SECTION_C, SECTION_C2)

def test_fit_course_empty():
    assert not scheduler.fit_course_in_schedules([set(SCHEDULE_A_LIST)], COURSE_A, SECTION_DICT)

def test_fit_course_nonempty():
    assert scheduler.fit_course_in_schedules([set()], COURSE_A, SECTION_DICT) == [{"10086"}, {'12580'}]

def test_schedule_course_empty():
    actual_schedules, error_string = scheduler.schedule_courses([COURSE_A, COURSE_B])
    expected_schedule = [[], [SECTION_A], [SECTION_A2], [SECTION_B], [SECTION_B2]]
    for schedule in expected_schedule:
        assert schedule in actual_schedules

    for schedule in actual_schedules:
        assert schedule in expected_schedule


