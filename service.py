from pathlib import Path



class Service:

    def __init__(self, url):
        self.__api = url.rstrip('/') + '/api'

    @property
    def main(self):
        return f'{self.__api}'
    
    @property
    def signup(self):
        return f'{self.__api}/signup'
    
    @property
    def signin(self):
        return f'{self.__api}/signin'
    
    @property
    def create_listing(self):
        return f'{self.__api}/create-listing'
    
    def edit_listing(self, id):
        return f'{self.__api}/update-offer/{id}'
    
    def delete_listing(self, id):
        return f'{self.__api}/listings/{id}'

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
IMG_PATH = ASSETS_DIR / "pancakes.jpg"
IMG_FALLBACK_URL = "https://qa-foodgram.s3.yandex.net/pancakes.jpg"


site = Service('https://qa-desk.stand.praktikum-services.ru')
