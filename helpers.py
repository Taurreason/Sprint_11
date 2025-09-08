import random
import string
from datetime import datetime
from pathlib import Path
import io
import requests
import allure


from data import *
from service import *



def headers_for_multipart(headers: dict) -> dict:
    """Убираем Content-Type: requests сам выставит boundary для multipart."""
    return {k: v for k, v in headers.items() if k.lower() != "content-type"}

def image_file(local_path: Path, fallback_url: str | None = None, mime="image/jpeg") -> dict:
    """
    Вернёт словарь для параметра files в requests.post.
    Если локального файла нет — при наличии fallback_url скачает в память.
    """
    if local_path.exists():
        return {"images": (local_path.name, local_path.open("rb"), mime)}
    if fallback_url:
        img_bytes = requests.get(fallback_url, timeout=15).content
        return {"images": ("image.jpg", io.BytesIO(img_bytes), mime)}
    raise FileNotFoundError(f"Нет файла: {local_path}")

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def build_user_payload(email, password, name):
    return {
        "email": email,
        "password": password,
        "submitPassword": name
    }

def generate_valid_unique_email(domain='yandexpr.ru'):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"testuser_{timestamp}@{domain}"

def generate_invalid_unique_email(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def headers_no_ct(h):
    return {k: v for k, v in h.items() if k.lower() != "content-type"}

def cleanup_delete(ann_id, headers):
    try:
        requests.delete(site.delete_listing(ann_id), headers=headers_no_ct(headers), timeout=15)
    except Exception:
        pass

def create_listing_as_owner(headers):
    files = image_file(IMG_PATH, fallback_url=IMG_FALLBACK_URL)
    mheaders = headers_for_multipart(headers)

    with allure.step("Владелец создаёт объявление"):
        resp = requests.post(site.create_listing, data=pancakes_data, files=files, headers=mheaders)
        assert resp.status_code == 201, f"{resp.status_code} {resp.text}"
    return resp.json()["id"]


def drop_ct(h):  # чтобы multipart/формы не ломались
    return {k: v for k, v in h.items() if k.lower() != "content-type"}
