from pathlib import Path


pancakes_data = {
    "name": "Блинчики",
    "category": "Хобби",
    "condition": "Новый",
    "city": "Москва",
    "description": "Готовим блинчики по бабушкиному рецепту каждый день!",
    "price": 1000
}

pancakes_data_edit = {
    "name": "Блинчики за миллион",
    "category": "Хобби",
    "condition": "Новый",
    "city": "Москва",
    "description": "Готовим блинчики по бабушкиному рецепту каждый день!",
    "price": 1000000
}

img_path = Path(__file__).parent / "assets" / "pancakes.jpg"
