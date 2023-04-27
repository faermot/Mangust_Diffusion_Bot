import requests


def translate(text):
    url = "https://translate.terraprint.co/translate"
    params = {"q": text,
              "source": "auto",
              "target": "en"}
    response = requests.post(url, params).json()
    prompt = response.get("translatedText")
    print(prompt)
    return prompt
