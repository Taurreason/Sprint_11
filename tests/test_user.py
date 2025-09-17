import allure, pytest
import requests

from service import site


@allure.epic("Создание пользователя")
@allure.feature("Создание пользователя")
class TestRegisterUser:


    @allure.title("Успешное создание уникального пользователя")
    def test_success_signup_user(self, user_data):
        with allure.step("Регистрация пользователя"):
            response = requests.post(site.signup, data=user_data)

        assert response.status_code == 201

    @allure.title("Создание существующего пользователя")
    def test_signup_user_already_exist(self, user_data):
        with allure.step("Регистрация пользователя"):
            response = requests.post(site.signup, data=user_data)
        with allure.step("Регистрация существующего пользователя"):
            response_exist = requests.post(site.signup, data=user_data)

        assert response_exist.status_code == 400 and response_exist.json().get("message") == 'Почта уже используется'


@allure.epic("Авторизация пользователя")
@allure.feature("Авторизация пользователя")
class TestLoginUser:

    @allure.title("Успешная авторизация пользователя")
    def test_success_signin_user(self, user_data):
        with allure.step("Регистрация пользователя"):
            signup_response = requests.post(site.signup, data=user_data)

        signin_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }

        with allure.step("Авторизация пользователя"):
            response = requests.post(site.signin, json=signin_data)
        
        body = response.json()
        token = body.get("token", {}).get("access_token")

        assert response.status_code == 201 and token
