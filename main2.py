import pytest



def create_courses_list(courses, mentors, durations):
    return [
        {"title": c, "mentors": m, "duration": d}
        for c, m, d in zip(courses, mentors, durations)
    ]


def get_sorted_courses_info(courses_list):
    durations_dict = {}
    for idx, course in enumerate(courses_list):
        durations_dict.setdefault(course["duration"], []).append(idx)

    result = []
    for duration in sorted(durations_dict.keys()):
        for idx in durations_dict[duration]:
            title = courses_list[idx]["title"]
            result.append(f"{title} - {duration} месяцев")
    return result



class TestCourseProcessing:

    @pytest.mark.parametrize("courses, mentors, durations, expected_len", [
        (["A", "B"], [["M1"], ["M2"]], [10, 20], 2),
        (["Python"], [["Иван"]], [5], 1),
        ([], [], [], 0),
    ])
    def test_create_courses_list(self, courses, mentors, durations, expected_len):
        result = create_courses_list(courses, mentors, durations)
        assert len(result) == expected_len
        if expected_len > 0:
            assert "title" in result[0] and "mentors" in result[0] and "duration" in result[0]

    @pytest.mark.parametrize("courses_list, expected_output", [
        (
                [
                    {"title": "Java-разработчик с нуля", "mentors": [], "duration": 14},
                    {"title": "Fullstack-разработчик на Python", "mentors": [], "duration": 20},
                    {"title": "Python-разработчик с нуля", "mentors": [], "duration": 12},
                    {"title": "Frontend-разработчик с нуля", "mentors": [], "duration": 20},
                ],
                [
                    "Python-разработчик с нуля - 12 месяцев",
                    "Java-разработчик с нуля - 14 месяцев",
                    "Fullstack-разработчик на Python - 20 месяцев",
                    "Frontend-разработчик с нуля - 20 месяцев",
                ]
        ),
        (
                [
                    {"title": "Курс A", "mentors": [], "duration": 5},
                    {"title": "Курс B", "mentors": [], "duration": 10},
                ],
                ["Курс A - 5 месяцев", "Курс B - 10 месяцев"]
        ),
        (
                [
                    {"title": "Первый", "mentors": [], "duration": 8},
                    {"title": "Второй", "mentors": [], "duration": 8},
                    {"title": "Третий", "mentors": [], "duration": 8},
                ],
                ["Первый - 8 месяцев", "Второй - 8 месяцев", "Третий - 8 месяцев"]
        ),
        ([], []),
    ])
    def test_get_sorted_courses_info(self, courses_list, expected_output):
        assert get_sorted_courses_info(courses_list) == expected_output

    @pytest.mark.parametrize("raw_courses, raw_mentors, raw_durations, expected_output", [
        (
                ["Java", "Fullstack"],
                [["Иван", "Анна"], ["Олег"]],
                [14, 20],
                ["Java - 14 месяцев", "Fullstack - 20 месяцев"]
        ),
        (
                ["C++", "Go", "Rust"],
                [[], [], []],
                [6, 3, 9],
                ["Go - 3 месяцев", "C++ - 6 месяцев", "Rust - 9 месяцев"]
        ),
    ])
    def test_full_pipeline(self, raw_courses, raw_mentors, raw_durations, expected_output):
        courses_list = create_courses_list(raw_courses, raw_mentors, raw_durations)
        result = get_sorted_courses_info(courses_list)
        assert result == expected_output