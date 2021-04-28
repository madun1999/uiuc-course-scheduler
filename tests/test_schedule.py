from course_scheduler_server.scheduler import scheduler
from course_scheduler_server.scheduler.scheduler_restriction import fit_course_in_schedules, RestrictionScheduler
# constants for testing
# meeting A collide with B
from scheduler.schedule import Schedule, make_annotated_section

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
    "part_of_term": "A",
    "meetings": [MEETING_C]
}
SECTION_C2 = {
    "section_id": "10001",
    "part_of_term": "B",
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
SCHEDULE_1 = Schedule()
SCHEDULE_1.add_section(make_annotated_section(SECTION_B, True))
SCHEDULE_1.add_section(make_annotated_section(SECTION_C, True))

COURSE_A = {
    "course_id": "CHOC123",
    "sections": [SECTION_A, SECTION_B]
}

COURSE_B = {
    "course_id": "BOX100",
    "sections": [SECTION_A2, SECTION_B2]
}

MANDATORY_COURSE_A = {
    "course": COURSE_A,
    "mandatory": True
}

MANDATORY_COURSE_B = {
    "course": COURSE_B,
    "mandatory": True
}

NOT_MANDATORY_COURSE_A = {
    "course": COURSE_A,
    "mandatory": False
}

NOT_MANDATORY_COURSE_B = {
    "course": COURSE_B,
    "mandatory": False
}

ALL_BREAK = {
    "start": "03:00 AM",
    "end": "10:00 PM",
    "days_of_the_week": "MTWRF",
}

ALL_BREAK_SECTION = {
    "section_id": -1,
    "part_of_term": "1",
    "meetings": []
}


def make_schedule(sections, mandatories):
    schedule = Schedule()
    for idx, section in enumerate(sections):
        schedule.add_section(make_annotated_section(section, mandatories[idx]))
    return schedule


def assert_schedule_lists_same(schedule_list_1, schedule_list_2):
    for schedule in schedule_list_1:
        assert schedule in schedule_list_2

    for schedule in schedule_list_2:
        assert schedule in schedule_list_1


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
    assert not fit_course_in_schedules({SCHEDULE_1}, MANDATORY_COURSE_A)


def test_fit_course_nonempty():
    actual_schedules = fit_course_in_schedules({Schedule()}, MANDATORY_COURSE_A)
    expected_schedule = [make_schedule([SECTION_A], [True]),
                         make_schedule([SECTION_B], [True]),
                         ]
    assert_schedule_lists_same(actual_schedules, expected_schedule)


def test_schedule_course_empty():
    restriction_scheduler = RestrictionScheduler(10, 0, [])
    actual_schedules, error_string = restriction_scheduler.schedule_courses([MANDATORY_COURSE_A, MANDATORY_COURSE_B])
    expected_schedule = [Schedule(),
                         make_schedule([SECTION_A], [True]),
                         make_schedule([SECTION_A2], [True]),
                         make_schedule([SECTION_B], [True]),
                         make_schedule([SECTION_B2], [True])]
    assert_schedule_lists_same(actual_schedules, expected_schedule)


def test_schedule_with_break():
    restriction_scheduler = RestrictionScheduler(10, 0, [ALL_BREAK])
    actual_schedules, error_string = restriction_scheduler.schedule_courses([MANDATORY_COURSE_A, MANDATORY_COURSE_B])
    expected_schedule = [make_schedule([ALL_BREAK_SECTION], [False])]
    assert_schedule_lists_same(expected_schedule, actual_schedules)


def test_schedule_with_max_courses():
    restriction_scheduler = RestrictionScheduler(0, 0, [])
    actual_schedules, error_string = restriction_scheduler.schedule_courses([MANDATORY_COURSE_A, MANDATORY_COURSE_B])
    expected_schedule = [Schedule()]
    assert_schedule_lists_same(actual_schedules, expected_schedule)


def test_schedule_with_min_mandatories():
    restriction_scheduler = RestrictionScheduler(10, 1, [])
    actual_schedules, error_string = restriction_scheduler.schedule_courses(
        [MANDATORY_COURSE_A, NOT_MANDATORY_COURSE_B])
    expected_schedule = [make_schedule([SECTION_A], [True]),
                         make_schedule([SECTION_B], [True])]
    assert_schedule_lists_same(actual_schedules, expected_schedule)
