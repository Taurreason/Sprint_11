import pytest, allure
from data import *
from helpers import *
from service import *


    
@pytest.fixture
def unique_valid_email():
    return generate_valid_unique_email()

@pytest.fixture
def unique_invalid_email():
    return generate_invalid_unique_email()

@pytest.fixture
def user_data(unique_valid_email):

    # генерируем имя, маил и пароль пользователя
    email = unique_valid_email
    password = generate_random_string(10)
    submitPassword = password

    # собираем тело запроса
    payload = build_user_payload(email, password, submitPassword)
    return payload

@pytest.fixture
def signup_signin_user(user_data):

    # Регистрация
    reg_response = requests.post(site.signup, json=user_data)

    # Авторизация
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    signin_response = requests.post(site.signin, json=login_data)
    body = signin_response.json()

    token = body.get("token", {}).get("access_token")
    assert token
    return { 
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
@pytest.fixture
def get_id_create_announcement(signup_signin_user):
        headers = headers_for_multipart(signup_signin_user)
        files = image_file(IMG_PATH, fallback_url=IMG_FALLBACK_URL)

        with allure.step("Создаем объявление"):
            ann_response = requests.post(site.create_listing, data=pancakes_data, headers=headers, files=files)

        assert ann_response.status_code == 201
        return ann_response.json()["id"]

@pytest.fixture
def make_auth_headers():
    """Фабрика: передай email/password/name — получишь headers с Bearer-токеном."""
    def _make(email: str, password: str, name: str) -> dict:
        reg = requests.post(site.signup, json={"email": email, "password": password, "name": name}, timeout=10)
        if reg.status_code not in (200, 201, 409):
            reg = requests.post(site.signup, data={"email": email, "password": password, "submitPassword": password, "name": name}, timeout=10)

        r = requests.post(site.signin, json={"email": email, "password": password}, timeout=10)
        token = r.json().get("token", {}).get("access_token")
        assert token, f"no token: {r.text}"
        return {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    return _make
