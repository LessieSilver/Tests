import pytest
import requests
import os

BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources/"

YANDEX_TOKEN = os.getenv("")


def api_request(method: str, path: str, token: str = YANDEX_TOKEN, **kwargs):
    headers = {"Authorization": f"OAuth {token}"}
    params = {"path": path}
    response = requests.request(method, BASE_URL, headers=headers, params=params, **kwargs)
    return response


@pytest.fixture
def test_folder_path():
    return "autotests/test_folder_pytest"


@pytest.fixture(autouse=True)
def cleanup(test_folder_path):
    yield
    try:
        api_request("DELETE", test_folder_path)
    except Exception:
        pass


class TestYandexDiskFolderAPI:

    def test_create_folder_success_and_verify(self, test_folder_path):
        put_resp = api_request("PUT", test_folder_path)
        assert put_resp.status_code in (200, 201), f"Ожидался 200/201, получен {put_resp.status_code}: {put_resp.text}"

        get_resp = api_request("GET", test_folder_path)
        assert get_resp.status_code == 200
        data = get_resp.json()
        assert data["type"] == "dir", "Созданный ресурс должен быть типа 'dir'"
        assert data["path"] == f"disk:/{test_folder_path}"

    @pytest.mark.parametrize("path, token, expected_code, description", [
        ("", YANDEX_TOKEN, 400, "Пустой путь"),
        ("test/invalid_auth_folder", "fake_token_12345", 401, "Невалидный OAuth-токен"),
    ])
    def test_create_folder_negative_cases(self, path, token, expected_code, description):
        resp = api_request("PUT", path, token=token)
        assert resp.status_code == expected_code, f"Тест '{description}': ожидался {expected_code}, получен {resp.status_code}"

    def test_create_folder_already_exists(self, test_folder_path):

        api_request("PUT", test_folder_path)
        resp = api_request("PUT", test_folder_path)
        assert resp.status_code == 409, "Повторное создание должно вернуть 409 Conflict"