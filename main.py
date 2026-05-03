import pytest
import copy



documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
    {"type": "driver license", "number": "5455 028765", "name": "Василий Иванов"},
]

directories = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006'],
    '3': []
}


def get_name(doc_number):
    for doc in documents:
        if doc["number"] == doc_number:
            return doc["name"]
    return "Документ не найден"


def get_directory(doc_number):
    for shelf, docs in directories.items():
        if doc_number in docs:
            return shelf
    return "Полки с таким документом не найдено"


def add(document_type, number, name, shelf_number):
    shelf_str = str(shelf_number)
    if shelf_str not in directories:
        directories[shelf_str] = []
    documents.append({
        "type": document_type,
        "number": number,
        "name": name
    })
    directories[shelf_str].append(number)



INITIAL_DOCUMENTS = copy.deepcopy(documents)
INITIAL_DIRECTORIES = copy.deepcopy(directories)


@pytest.fixture(autouse=True)
def reset_state():
    documents[:] = copy.deepcopy(INITIAL_DOCUMENTS)
    directories.clear()
    directories.update(copy.deepcopy(INITIAL_DIRECTORIES))
    yield


class TestDocumentSystem:

    @pytest.mark.parametrize("doc_number, expected_name", [
        ("2207 876234", "Василий Гупкин"),
        ("10006", "Аристарх Павлов"),
        ("5455 028765", "Василий Иванов"),
        ("999999", "Документ не найден"),
    ])
    def test_get_name(self, doc_number, expected_name):
        assert get_name(doc_number) == expected_name

    @pytest.mark.parametrize("doc_number, expected_shelf", [
        ("11-2", "1"),
        ("10006", "2"),
        ("2207 876234", "1"),
        ("888888", "Полки с таким документом не найдено"),
    ])
    def test_get_directory(self, doc_number, expected_shelf):
        assert get_directory(doc_number) == expected_shelf

    @pytest.mark.parametrize("doc_type, number, name, shelf", [
        ("international passport", "311 020203", "Александр Пушкин", "3"),
        ("visa", "000-000", "Тестовый Пользователь", "99"),
    ])
    def test_add(self, doc_type, number, name, shelf):
        shelf_key = str(shelf)

        add(doc_type, number, name, shelf)

        added_doc = next((d for d in documents if d["number"] == number), None)
        assert added_doc is not None, "Документ не добавлен в documents"
        assert added_doc["type"] == doc_type
        assert added_doc["name"] == name

        assert shelf_key in directories, f"Полка {shelf_key} не создана в directories"
        assert number in directories[shelf_key], f"Номер {number} не найден на полке {shelf_key}"