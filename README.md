Mangust Diffusion Bot 
=

![Python](images/python_icon.svg)


[Телеграм бот](https://t.me/mangust_diffusion_bot) для генерации изображений по запросу при помощи Stable Diffusion

## Установка

```python
git clone https://github.com/faermot/Mangust_Diffusion_Bot.git
```

Создайте `.venv` и вставьте в его следущее:
```commandline
BOT_TOKEN = ТОКЕН БОТА
URI = "ВАШ-API-MONGODB"
URL = "http://127.0.0.1:7860"
```

И запустите main.py 
>У вас должен быть локально установлен и запущен запущен Stable Diffusion, 
> или же у вас должна быть публичная ссылка запущенной модели.


## Технологии 
- Python 3.10
- Aiogram 2.23.1
> Подробнее в requirements.txt