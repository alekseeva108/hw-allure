"""
Автотесты для сервиса PostmanEcho (https://postman-echo.com)
Проверяют поведение GET и POST эндпоинтов.

Запуск:
    python3 -m pytest -v --tb=short --alluredir=allure-reports
    allure serve allure-reports
"""

import allure

from utils.api_client import EchoClient
from utils.helpers import assert_status, assert_field_equals, assert_key_exists


@allure.epic('PostmanEcho API')
@allure.feature('GET /get')
class TestGetRequests:

    @allure.title('GET /get возвращает статус 200')
    @allure.description('Базовый GET-запрос без параметров должен вернуть HTTP 200.')
    def test_get_status_code(self):
        client = EchoClient()
        response = client.get()
        assert_status(response, 200)

    @allure.title('GET /get возвращает валидный JSON')
    @allure.description('Ответ должен быть корректным JSON-объектом (словарём).')
    def test_get_response_is_json(self):
        client = EchoClient()
        response = client.get()
        assert_status(response, 200)
        data = response.json()
        with allure.step('Проверка, что ответ является словарём'):
            assert isinstance(data, dict), f'Ожидался dict, получен {type(data)}'

    @allure.title('GET /get отражает query-параметры')
    @allure.description('Переданные query-параметры должны вернуться в поле "args" ответа.')
    def test_get_with_query_params(self, query_params):
        client = EchoClient()
        response = client.get(params=query_params)
        assert_status(response, 200)

        data = response.json()
        assert_key_exists(data, 'args')
        assert_field_equals(data['args'], 'foo', 'bar')
        assert_field_equals(data['args'], 'num', '42')

    @allure.title('GET /get содержит поле url в ответе')
    @allure.description('Тело ответа должно содержать поле "url" с адресом запроса.')
    def test_get_url_field_in_response(self):
        client = EchoClient()
        response = client.get()
        assert_status(response, 200)

        data = response.json()
        assert_key_exists(data, 'url')
        with allure.step('Проверка, что url содержит postman-echo.com/get'):
            assert 'postman-echo.com/get' in data['url'], \
                f'Неожиданный url: {data["url"]}'

    @allure.title('GET /get отражает кастомные заголовки запроса')
    @allure.description('Заголовки из запроса должны вернуться в поле "headers" ответа.')
    def test_get_headers_reflected(self, custom_headers):
        client = EchoClient()
        response = client.get(headers=custom_headers)
        assert_status(response, 200)

        data = response.json()
        assert_key_exists(data, 'headers')
        with allure.step('Проверка значения X-Custom-Header'):
            actual = data['headers'].get('x-custom-header')
            assert actual == 'hello-test', \
                f'Ожидалось "hello-test", получено "{actual}"'


@allure.epic('PostmanEcho API')
@allure.feature('POST /post')
class TestPostRequests:

    @allure.title('POST /post возвращает статус 200')
    @allure.description('Базовый POST-запрос без тела должен вернуть HTTP 200.')
    def test_post_status_code(self):
        client = EchoClient()
        response = client.post()
        assert_status(response, 200)

    @allure.title('POST /post отражает JSON-тело запроса')
    @allure.description('Переданный JSON должен вернуться в поле "json" ответа.')
    def test_post_with_json_body(self, json_payload):
        client = EchoClient()
        response = client.post(json=json_payload)
        assert_status(response, 200)

        data = response.json()
        assert_key_exists(data, 'json')
        assert_field_equals(data['json'], 'name', 'Alice')
        assert_field_equals(data['json'], 'age', 30)

    @allure.title('POST /post отражает form-data')
    @allure.description('Переданные form-данные должны вернуться в поле "form" ответа.')
    def test_post_with_form_data(self, form_data):
        client = EchoClient()
        response = client.post(data=form_data)
        assert_status(response, 200)

        data = response.json()
        assert_key_exists(data, 'form')
        assert_field_equals(data['form'], 'username', 'testuser')
        assert_field_equals(data['form'], 'password', 'secret')

    @allure.title('POST /post с JSON содержит правильный Content-Type')
    @allure.description(
        'При отправке JSON заголовок Content-Type должен быть application/json '
        '— это подтверждается отражёнными заголовками в ответе.'
    )
    def test_post_content_type_json(self):
        client = EchoClient()
        response = client.post(json={"key": "value"})
        assert_status(response, 200)

        data = response.json()
        assert_key_exists(data, 'headers')
        with allure.step('Проверка Content-Type в отражённых заголовках'):
            content_type = data['headers'].get('content-type', '')
            assert 'application/json' in content_type, \
                f'Неожиданный Content-Type: "{content_type}"'

    @allure.title('POST /post принимает query-параметры и JSON одновременно')
    @allure.description(
        'Запрос с query-параметрами и JSON-телом должен вернуть оба набора данных '
        'в соответствующих полях "args" и "json".'
    )
    def test_post_with_query_params_and_body(self):
        client = EchoClient()
        response = client.post(params={"source": "pytest"}, json={"message": "hello"})
        assert_status(response, 200)

        data = response.json()
        assert_key_exists(data, 'args')
        assert_field_equals(data['args'], 'source', 'pytest')
        assert_key_exists(data, 'json')
        assert_field_equals(data['json'], 'message', 'hello')
