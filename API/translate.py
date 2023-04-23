import google_translate_api_python
a=google_translate_api_python.GoogleTranslate(domainnames="ru", sl="ru", tl="en")
print(a.trans("Hello World."))