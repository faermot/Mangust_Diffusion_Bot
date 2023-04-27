import requests
from io import BytesIO


def get_cat():
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    url = response.json()[0]['url']
    response = requests.get(url)
    photo_cat = BytesIO(response.content)
    return photo_cat