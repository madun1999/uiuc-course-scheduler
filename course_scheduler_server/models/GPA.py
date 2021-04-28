from typing import TypedDict, List


class GPA(TypedDict):
    """GPA information of a section"""
    average: float
    a_rate: float


GRADE_TO_GPA = [4.0, 4.0, 3.67, 3.33, 3.00, 2.67, 2.33, 2.0, 1.67, 1.33, 1.0, 0.67, 0.0, 0.0]


def calculate_gpa(mean_grades: List[float]) -> GPA:
    """
    Calculates GPA from mean_grades
    :param mean_grades: List of mean grades, A+, A, A-, B+, B, B-, C+, C, C-, D+, D, D-, F, W
    :return: GPA
    """
    average = sum(x * y for x, y in zip(mean_grades, GRADE_TO_GPA)) / sum(mean_grades)
    a_rate = (mean_grades[0] + mean_grades[1]) / sum(mean_grades)
    return {
        "average": average,
        "a_rate": a_rate
    }
