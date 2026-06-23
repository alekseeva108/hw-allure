import allure
import pytest


@pytest.fixture
@allure.step('Подготовка query-параметров')
def query_params():
    return {"foo": "bar", "num": "42"}


@pytest.fixture
@allure.step('Подготовка JSON-тела запроса')
def json_payload():
    return {"name": "Alice", "age": 30}


@pytest.fixture
@allure.step('Подготовка form-данных')
def form_data():
    return {"username": "testuser", "password": "secret"}


@pytest.fixture
@allure.step('Подготовка кастомных заголовков')
def custom_headers():
    return {"X-Custom-Header": "hello-test"}
