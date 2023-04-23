from dotenv import load_dotenv
load_dotenv()

import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
import access_bot as ab
import keyboard as kb
import API.stable_diffusion as sd
import database.functions as df
import enchant

import logging

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



class AccessKey(StatesGroup):
    waiting_for_key = State()


@dp.message_handler(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    if not os.path.exists("Users\\" + str(user_id) + "\\key_true"):
        await bot.send_message(message.from_user.id, "Введите код доступа:")
        await AccessKey.waiting_for_key.set()
    else:
        await bot.send_message(
            message.from_user.id,
            "*Доступ разрешён.* \n"
            "💡 Советуем ознакомится с ботом, используя /help \n"
            "Составь максимально точный запрос, и отправь его в бота. "
            "От точности запроса зависит качество генерации изображения. \n"
            "\nЧто бы получить пример такого запроса, воспользуйся кнопкой ниже.\n"
            "\nБот понимает запросы на английском языке. ",
            parse_mode="Markdown",
            reply_markup=kb.start_menu
        )


@dp.message_handler(state=AccessKey.waiting_for_key)
async def process_key(message: types.Message, state: FSMContext):
    keys = ab.get_keys()
    key = message.text
    user_id = ab.get_user_id(message)
    used_keys = ab.get_used_keys()
    if key in keys and key not in used_keys:
        ab.set_used_key(key)
        os.mkdir("Users\\" + user_id)
        with open("Users\\" + user_id + "\\key_true", 'w+') as f:
            f.write(key)
        await state.finish()
        name = message.from_user.username
        df.create_user_in_db(user_id, name)
        await message.reply(
            "*Доступ разрешён.* \n"
            "💡 Советуем ознакомится с ботом, используя /help \n"
            "Составь максимально точный запрос, и отправь его в бота. "
            "От точности запроса зависит качество генерации изображения. \n"
            "\nЧто бы получить пример такого запроса, воспользуйся кнопкой ниже.\n"
            "\nБот понимает запросы только на английском языке. ",
            parse_mode="Markdown",
            reply_markup=kb.start_menu
        )
        await message.delete()

    elif key in used_keys:
        await message.reply("Этот код уже используется другим пользователем.")
    else:
        await message.reply("Неверный код доступа. Попробуйте ещё раз.")


@dp.callback_query_handler(lambda callback_query: True)
async def callback_handler(callback: types.CallbackQuery):
    sampling_methods = ["Euler a", "Euler", "LMS", "DPM2", "DPM adaptive", "DDIM"]
    styles = ["Anime",
              "Manga",
              "Photo",
              "Pixel art",
              "Cyberpunk",
              "Sketch",
              "SmoothFace",
              "Macro-Photo",
              "Fantasy",
              "no_style"
              ]
    sampling_steps = ["10", "14", "16", "20", "23", "25", "30", "35", "40", "45", "50", "55"]
    cfg_scale = ["1.0", "3.0", "5.0", "7.0", "9.0", "11.0", "13.0", "15.0", "19.0", "26.0", "29.0", "34.0"]
    models = ["midj", "revAnim", "pruned"]
    if callback.data == "get_example":
        example = open("example.png", 'rb')
        await callback.message.answer_photo(
            example,
            "anime, hand-drawn and cel animation techniques,"
            " (fishing boat sailing on waves during storm), "
            "natural design, beautifully rendered and expressive rich colors, "
            "vibrant pastel colors, imaginative and fantastical landscapes, "
            "sharp attention to detail, "
            "realism and a strong sense of nostalgia and warmth, "
            "sharp attention to small details and textures, fantastical creatures, settings, "
            "depth and emotions emphasized and accentuated by lighting and shading, "
            "extremely high quality, incredibly high finite definition, high resolution, "
            "hand-drawn and cel animation techniques,"
        )
        example.close()

    elif callback.data == "styles":
        await callback.message.edit_text(
            "⭐ Выберите стиль (по умолчанию без стиля):",
            reply_markup=kb.style_button
        )

    elif callback.data == "sampling_method":
        await callback.message.edit_text(
            "🌌 Выберите метод отбора (по умолчанию Euler a):",
            reply_markup=kb.sampling_method_menu
        )

    elif callback.data in sampling_methods:
        user_id = ab.get_user_id(callback)
        param = "sampler_index"
        value = str(callback.data)
        df.add_argument_to_user(user_id, param, value)
        await callback.message.edit_text(
            "*✅ Успешно.* \nВы можете продолжить настраивать параметры, или начать генерацию.",
            reply_markup=kb.params_menu,
            parse_mode="Markdown"
        )

    elif callback.data == "sampling_steps":
        await callback.message.edit_text(
            "🥇 Выберите значение выборки (по умолчанию 20.0, советуем не выставлять слишком высокие значения):",
            reply_markup=kb.sampling_steps_button
        )

    elif callback.data in sampling_steps:
        user_id = ab.get_user_id(callback)
        param = "steps"
        value = callback.data
        df.add_argument_to_user(user_id, param, int(value))
        await callback.message.edit_text(
            "*✅ Успешно.* \nВы можете продолжить настраивать параметры, или начать генерацию.",
            reply_markup=kb.params_menu,
            parse_mode="Markdown"
        )

    elif callback.data in styles:
        user_id = ab.get_user_id(callback)
        if callback.data == "no_style":
            value = " "

        else:
            value = str(callback.data)
        new_data = df.add_style_to_user(user_id, value.split())
        try:
            await callback.message.edit_text(
                "*✅ Стиль успешно применён.* \nВы можете продолжить настраивать параметры, или начать генерацию.",
                reply_markup=kb.params_menu,
                parse_mode="Markdown"
            )
        except:
            pass

    elif callback.data == "cfg_scale":
        await callback.message.edit_text(
            "📊 Выберите значение CFG (по умолчанию 7.0, советуем не выставлять слишком высокие значения):",
            reply_markup=kb.cfg_scale_button
        )

    elif callback.data in cfg_scale:
        user_id = ab.get_user_id(callback)
        param = "cfg_scale"
        value = callback.data
        new_data = df.add_argument_to_user(user_id, param, float(value))
        await callback.message.edit_text(
            "✅ Успешно. \nВы можете продолжить настраивать параметры, или начать генерацию.",
            reply_markup=kb.params_menu
        )

    elif callback.data == "set_default":
        user_id = ab.get_user_id(callback)
        df.set_default_params(user_id)
        await callback.message.edit_text(
            "*✅ Установлены параметры по умолчанию.* \nВы можете продолжить настраивать параметры, или начать генерацию.",
            reply_markup=kb.params_menu,
            parse_mode="Markdown"
        )

    elif callback.data == "back_in_menu":
        await callback.message.edit_text(
            "*✅ Успешно. *\nВы можете продолжить настраивать параметры, или начать генерацию.",
            reply_markup=kb.params_menu,
            parse_mode="Markdown"
        )

    elif callback.data == "model":
        await callback.message.edit_text(
            "🤖 Выберите модель:",
            reply_markup=kb.models_menu
        )

    elif callback.data in models:
        user_id = ab.get_user_id(callback)
        param = "model_name"
        if callback.data == "midj":
            value = "ANYTHING_MIDJOURNEY_V_4.1.ckpt [041eabfcc6]"
            new_data = df.set_model_to_user(user_id, value)
        elif callback.data == "revAnim":
            value = "revAnimated_v122.safetensors [f8bb2922e1]"
            new_data = df.set_model_to_user(user_id, value)

        elif callback.data == "pruned":
            value = "v1-5-pruned.ckpt [e1441589a6]"

        await callback.message.edit_text(
            "*✅ Успешно. *\nВы можете продолжить настраивать параметры, или начать генерацию.",
            reply_markup=kb.params_menu,
            parse_mode="Markdown"
        )


    elif callback.data == "resume":
        await callback.message.edit_text(
            "✅ В обработке..."
        )
        user_id = ab.get_user_id(callback)
        photo = sd.render_photo(user_id)
        await callback.message.delete()
        await bot.send_photo(callback.from_user.id, photo)


@dp.message_handler(content_types=['text'])
async def generate_photo(message: types.Message):
    prompt = message.text
    user_id = ab.get_user_id(message)
    df.add_prompt_to_user(user_id, prompt)
    await bot.send_message(
        message.chat.id,
        "🌄 Вы можете настроить генерацию, используя кнопки ниже,"
        "или пропустить этот шаг. В таком случае будут использованы "
        "стандартные настройки.",
        reply_markup=kb.params_menu)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

