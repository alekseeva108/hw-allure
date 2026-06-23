import allure
import requests

BASE_URL = "https://postman-echo.com"


class EchoClient:

    @allure.step('GET-запрос к /get')
    def get(self, params=None, headers=None):
        url = f"{BASE_URL}/get"
        response = requests.get(url, params=params, headers=headers)

        allure.attach(url, name='URL', attachment_type=allure.attachment_type.TEXT)
        if params:
            allure.attach(str(params), name='Query params', attachment_type=allure.attachment_type.TEXT)
        if headers:
            allure.attach(str(headers), name='Request headers', attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name='Response JSON', attachment_type=allure.attachment_type.JSON)

        return response

    @allure.step('POST-запрос к /post')
    def post(self, params=None, json=None, data=None):
        url = f"{BASE_URL}/post"
        response = requests.post(url, params=params, json=json, data=data)

        allure.attach(url, name='URL', attachment_type=allure.attachment_type.TEXT)
        if json:
            allure.attach(str(json), name='JSON payload', attachment_type=allure.attachment_type.TEXT)
        if data:
            allure.attach(str(data), name='Form data', attachment_type=allure.attachment_type.TEXT)
        if params:
            allure.attach(str(params), name='Query params', attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name='Response JSON', attachment_type=allure.attachment_type.JSON)

        return response
