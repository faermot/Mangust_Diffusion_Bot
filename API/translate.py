import requests


def check_language(no_translated_prompt):
    count = 0
    for char in no_translated_prompt:
        if char.isalpha() and char.islower():
            count += 1
    if count > 5:
        prompt = no_translated_prompt
        return  prompt
    else:
        prompt = translate(no_translated_prompt)
        return prompt


def translate(text):
    url = "https://translate.terraprint.co/translate"
    params = {"q": text,
              "source": "auto",
              "target": "en"}
    response = requests.post(url, params).json()
    prompt = response.get("translatedText")
    print(prompt)
    return prompt
