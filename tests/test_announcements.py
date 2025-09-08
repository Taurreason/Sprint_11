import allure, pytest
import requests

from service import *
from data import *
from helpers import *


@allure.epic("Объявления")
@allure.feature("Объявления")
class TestAnnouncement:


    @allure.title("Создание объявления")
    def test_create_announcement(self, signup_signin_user):

        headers = headers_for_multipart(signup_signin_user)
        files = image_file(IMG_PATH, fallback_url=IMG_FALLBACK_URL)

        with allure.step("Создаем объявление"), img_path.open("rb") as f:
            ann_response = requests.post(site.create_listing, data=pancakes_data, headers=headers, files=files)

        body = ann_response.json()
        assert ann_response.status_code == 201 and body.get("name") == pancakes_data["name"]

    @allure.title("Редактирование объявления")
    def test_edit_announcement(self, get_id_create_announcement, signup_signin_user):
        headers = {k: v for k, v in signup_signin_user.items() if k.lower() != "content-type"}

        response = requests.patch(site.edit_listing(get_id_create_announcement),
                                  data=pancakes_data_edit,
                                  headers=headers)
        
        assert response.status_code == 200 and response.json().get("name") == pancakes_data_edit["name"] and response.json().get("id") == get_id_create_announcement

    @allure.title("Удаление объявления")
    def test_delete_announcement(self, get_id_create_announcement, signup_signin_user):
        headers = {k: v for k, v in signup_signin_user.items() if k.lower() != "content-type"}

        response = requests.delete(site.delete_listing(get_id_create_announcement), headers=headers)

        assert response.status_code == 200 and response.json().get("message") == 'Объявление удалено успешно'

    @allure.title("Редактирование чужого объявления запрещено")
    def test_edit_foreign_announcement(self, get_id_create_announcement, signup_signin_user):
        ann_id = get_id_create_announcement
        owner_headers = {k: v for k, v in signup_signin_user.items() if k.lower() != "content-type"}

        # заводим 'чужого' пользователя прямо в тесте
        email2 = generate_valid_unique_email("yandexpr.ru")
        pwd2 = "Qwer1234!"
        reg = requests.post(site.signup, json={"email": email2, "password": pwd2, "name": "Stranger"})

        r = requests.post(site.signin, json={"email": email2, "password": pwd2})
        token2 = r.json().get("token", {}).get("access_token")
        stranger_headers = {"Authorization": f"Bearer {token2}", "Accept": "application/json"}
        stranger_headers = {k: v for k, v in stranger_headers.items() if k.lower() != "content-type"}

        # попытка редактирования чужим пользователем
        patch_data = {"name": "Блинчики (ред.)", "price": "999"}
        with allure.step("Чужой пользователь пытается редактировать"):
            resp_forbidden = requests.patch(
                site.edit_listing(ann_id),
                data=patch_data, 
                headers=stranger_headers,
                timeout=30
            )
        assert resp_forbidden.status_code == 401
