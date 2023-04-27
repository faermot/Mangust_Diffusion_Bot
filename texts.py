from aiogram.utils.markdown import link

first_message = "*Доступ разрешён.* \n" \
                "💡 Советуем ознакомится с ботом, используя /help \n" \
                "Составь максимально точный запрос, и отправь его в бота. " \
                "От точности запроса зависит качество генерации изображения. \n" \
                "\nЧто бы получить пример такого запроса, воспользуйся кнопкой ниже.\n" \
                "\nБот понимает запросы только на английском языке. "

link_1 = link('статье', 'https://telegra.ph/Mangust-Diffusion-Bot-04-26')

start_message = "*Доступ разрешён.* \n" \
                f"💡 Советуем ознакомится с ботом, прочитав {link_1}.\n" \
                "Составь максимально точный запрос, и отправь его в бота. " \
                "От точности запроса зависит качество генерации изображения. \n" \
                "\nЧто бы получить пример такого запроса, воспользуйся кнопкой ниже.\n" \
                "\nНе смотря на то что бот понимает запросы и на русском, " \
                "настоятельно рекомендуем использовать английский."

start_menu = "🎯 Составь максимально точный запрос, и отправь его в бота. " \
             "От точности запроса зависит качество генерации изображения. \n" \
             "\nЧто бы получить пример такого запроса, воспользуйся кнопкой ниже.\n" \
             "\nНе смотря на то что бот понимает запросы и на русском, " \
             "настоятельно рекомедуем использовать английский."

link_2 = link('статье', 'https://telegra.ph/Mangust-Diffusion-Bot-04-26')

help_message = f"*📖 Справка по боту* \n*Версия бота*: 2.0 \n" \
               f"Все найденные недоработки и баги отправлять @faermot \n\n" \
               f"Ознакомиться с ботом можно в {link_2} ниже."

main_menu_message = "🌄 Вы можете настроить генерацию, используя кнопки ниже," \
                    "или пропустить этот шаг. В таком случае будут использованы " \
                    "стандартные настройки."

example_caption = "anime, hand-drawn and cel animation techniques," \
                  " (fishing boat sailing on waves during storm), " \
                  "natural design, beautifully rendered and expressive rich colors, " \
                  "vibrant pastel colors, imaginative and fantastical landscapes, " \
                  "sharp attention to detail, " \
                  "realism and a strong sense of nostalgia and warmth, " \
                  "sharp attention to small details and textures, fantastical creatures, settings, " \
                  "depth and emotions emphasized and accentuated by lighting and shading, " \
                  "extremely high quality, incredibly high finite definition, high resolution, " \
                  "hand-drawn and cel animation techniques,"

sticker = "CAACAgIAAxkBAAEIvfpkSXR0cY6-F5MakAfTp-LeCar-AgACQzAAAplZSEqbc3Vq1yevsC8E"