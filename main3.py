import pytest



def extract_first_names(mentors):
    all_list = []
    for m in mentors:
        all_list += m
    return [mentor.split()[0] for mentor in all_list]

def get_top_mentors_counts(first_names, top_n=3):
    unique_names = set(first_names)
    popular = [[name, first_names.count(name)] for name in unique_names]
    popular.sort(key=lambda x: x[1], reverse=True)
    return popular[:top_n]

def format_top_mentors(top_list):
    return ", ".join(f"{name}: {count} раз(а)" for name, count in top_list)



class TestMentorAnalysis:

    @pytest.mark.parametrize("mentors, expected", [
        ([["Иван Иванов", "Петр Петров"], ["Анна Сидорова"]], ["Иван", "Петр", "Анна"]),
        ([["Александр Пушкин"]], ["Александр"]),
        ([[], []], []),
    ])
    def test_extract_first_names(self, mentors, expected):
        assert extract_first_names(mentors) == expected

    @pytest.mark.parametrize("first_names, top_n, expected", [
        (["А", "А", "Б", "Б", "Б", "В", "Г", "Д"], 3, [["Б", 3], ["А", 2], ["В", 1]]),
        (["Иван", "Иван", "Олег"], 1, [["Иван", 2]]),
        (["А", "Б"], 5, [["А", 1], ["Б", 1]]),
        ([], 3, []),
    ])
    def test_get_top_mentors_counts(self, first_names, top_n, expected):
        assert get_top_mentors_counts(first_names, top_n) == expected

    @pytest.mark.parametrize("top_list, expected", [
        ([["Александр", 10], ["Евгений", 5]], "Александр: 10 раз(а), Евгений: 5 раз(а)"),
        ([["Тест", 1]], "Тест: 1 раз(а)"),
        ([], ""),
    ])
    def test_format_top_mentors(self, top_list, expected):
        assert format_top_mentors(top_list) == expected

    def test_full_pipeline_original_data(self):
        mentors = [
            ["Евгений Шмаргунов", "Олег Булыгин", "Дмитрий Демидов", "Кирилл Табельский", "Александр Ульянцев", "Александр Бардин", "Александр Иванов", "Антон Солонилин", "Максим Филипенко", "Елена Никитина", "Азамат Искаков", "Роман Гордиенко"],
            ["Филипп Воронов", "Анна Юшина", "Иван Бочаров", "Анатолий Корсаков", "Юрий Пеньков", "Илья Сухачев", "Иван Маркитан", "Ринат Бибиков", "Вадим Ерошевичев", "Тимур Сейсембаев", "Максим Батырев", "Никита Шумский", "Алексей Степанов", "Денис Коротков", "Антон Глушков", "Сергей Индюков", "Максим Воронцов", "Евгений Грязнов", "Константин Виролайнен", "Сергей Сердюк", "Павел Дерендяев"],
            ["Евгений Шмаргунов", "Олег Булыгин", "Александр Бардин", "Александр Иванов", "Кирилл Табельский", "Александр Ульянцев", "Роман Гордиенко", "Адилет Асканжоев", "Александр Шлейко", "Алена Батицкая", "Денис Ежков", "Владимир Чебукин", "Эдгар Нуруллин", "Евгений Шек", "Максим Филипенко", "Елена Никитина"],
            ["Владимир Чебукин", "Эдгар Нуруллин", "Евгений Шек", "Валерий Хаслер", "Татьяна Тен", "Александр Фитискин", "Александр Шлейко", "Алена Батицкая", "Александр Беспоясов", "Денис Ежков", "Николай Лопин", "Михаил Ларченко"]
        ]

        first_names = extract_first_names(mentors)
        top_3 = get_top_mentors_counts(first_names, top_n=3)
        result_string = format_top_mentors(top_3)

        expected_string = "Александр: 10 раз(а), Евгений: 5 раз(а), Максим: 4 раз(а)"
        assert result_string == expected_string