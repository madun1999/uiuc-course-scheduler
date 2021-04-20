import pandas as pd
from course_scheduler_server.db.db_gpa_handler import post_course_gpas


def parse_course_gpas(file='../uiuc-gpa-dataset.csv'):
    gpa_df = pd.read_csv(file)

    all_course_gpas = []

    # group by course
    for course_group, course_name in gpa_df.groupby(['Subject', 'Number']):

        # group by instructors in one course
        instructors = []
        for instructor_group, instructor_name in course_name.groupby(['Primary Instructor']):
            instructor_split = instructor_group.split(', ')

            # group by terms in one instructor
            terms = []
            for term_group, term_name in instructor_name.groupby(['YearTerm']):
                term = {
                    'year': term_group[:4],
                    'semester': term_group[5:],
                    'grades': list(term_name.mean())[2:]
                }
                terms.append(term)

            instructor = {
                'first_name': instructor_split[1],
                'last_name': instructor_split[0],
                'mean_grades': list(instructor_name.mean()[2:]),
                'term_mean_grades': terms
            }
            instructors.append(instructor)

        course_gpas = {
            'course_id': course_group[0] + " " + str(course_group[1]),
            'instructor_grades': instructors
        }
        all_course_gpas.append(course_gpas)
    return all_course_gpas


def add_course_gpas_to_db(file='../uiuc-gpa-dataset.csv'):
    all_course_gpas = parse_course_gpas(file)
    for course_gpas in all_course_gpas:
        post_course_gpas(course_gpas)


if __name__ == "__main__":
    """
    For demo and testing 
    """
    add_course_gpas_to_db()
