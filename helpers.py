import io
import random
import string
from datetime import datetime
from pathlib import Path

import requests


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
