import allure


@allure.step('Проверка статуса ответа: ожидается {expected_status}')
def assert_status(response, expected_status):
    assert response.status_code == expected_status, \
        f'Ожидался статус {expected_status}, но получен {response.status_code}'


@allure.step('Проверка поля "{field}" в ответе')
def assert_field_equals(data, field, expected_value):
    assert data[field] == expected_value, \
        f'Ожидалось {field}={expected_value!r}, но получено {data[field]!r}'


@allure.step('Проверка наличия ключа "{key}" в ответе')
def assert_key_exists(data, key):
    assert key in data, f'Ключ "{key}" отсутствует в ответе: {data}'
