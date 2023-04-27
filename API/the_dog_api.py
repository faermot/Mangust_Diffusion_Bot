import requests
from io import BytesIO


def get_dog():
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    url = response.json()['message']
    response = requests.get(url)
    photo_dog = BytesIO(response.content)
    return photo_dog