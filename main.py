import requests
from dotenv import load_dotenv
load_dotenv()
import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
import get_user_id as g
import access_bot as ab
import keyboard as kb
import API.stable_diffusion as sd
import database.functions as df
import API.translate as tr
import API.the_cat_api as gcat
import API.the_dog_api as gdog
import texts as t
import lists as list
import logging

logging.basicConfig(level=logging.INFO)

BOT_TOKEN: str | None = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class AccessKey(StatesGroup):
    waiting_for_key = State()


class Form(StatesGroup):
    text = State()


@dp.message_handler(Command('start'))
async def cmd_start(message: types.Message):
    user_id = message.chat.id
    answer = df.check_key(user_id)
    if not answer == True:
        await bot.send_message(message.from_user.id, "Введите код доступа:")
        await AccessKey.waiting_for_key.set()
    else:
        await bot.send_message(
            message.from_user.id,
            t.start_message,
            parse_mode="Markdown",
            reply_markup=kb.start_menu
        )


@dp.message_handler(state=AccessKey.waiting_for_key)
async def process_key(message: types.Message, state: FSMContext):
    keys = ab.get_keys()
    key = message.text
    user_id = g.get_user_id(message)
    used_keys = ab.get_used_keys()
    if key in keys and key not in used_keys:
        name = message.from_user.username
        df.create_user_in_db(user_id, name)
        await message.reply(
            t.first_message,
            parse_mode="Markdown",
            reply_markup=kb.start_menu
        )
        await state.finish()
        await message.delete()

    elif key in used_keys:
        await message.reply("Этот код уже используется другим пользователем.")
    else:
        await message.reply("Неверный код доступа. Попробуйте ещё раз.")


@dp.message_handler(Command('start_menu'))
async def start_menu(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        t.start_menu,
        parse_mode="Markdown",
        reply_markup=kb.start_menu
    )


@dp.message_handler(Command('help'))
async def help_menu(message: types.Message):
    await bot.send_message(
        message.chat.id,
        t.help_message,
        parse_mode="Markdown"
    )


@dp.message_handler(Command('menu'))
async def main_menu(message: types.Message):
    await bot.send_message(
        message.chat.id,
        t.main_menu_message,
        reply_markup=kb.params_menu
    )


@dp.message_handler(Command('cat'))
async def random_cat(message: types.Message):
    msg = await message.reply("🐈")
    cat_photo = gcat.get_cat()
    await msg.delete()
    await bot.send_photo(message.from_user.id, cat_photo)


@dp.message_handler(Command('dog'))
async def random_dog(message: types.Message):
    msg = await message.reply("🐶")
    dog_photo = gdog.get_dog()
    await msg.delete()
    await bot.send_photo(message.from_user.id, dog_photo)


@dp.callback_query_handler(lambda callback_query: True)
async def callback_handler(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "get_example":
        example = open("example.png", 'rb')
        await callback.message.answer_photo(
            example,
            t.example_caption
        )
        example.close()

    elif callback.data == "sampling_method":
        await callback.message.edit_text(
            "🌌 Выберите метод отбора (по умолчанию Euler a):",
            reply_markup=kb.sampling_method_menu
        )

    elif callback.data in list.sampling_methods:
        user_id = g.get_user_id(callback)
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

    elif callback.data in list.sampling_steps:
        user_id = g.get_user_id(callback)
        param = "steps"
        value = callback.data
        df.add_argument_to_user(user_id, param, int(value))
        await callback.message.edit_text(
            "*✅ Успешно.* \nВы можете продолжить настраивать параметры, или начать генерацию.",
            reply_markup=kb.params_menu,
            parse_mode="Markdown"
        )

    elif callback.data == "styles":
        await callback.message.edit_text(
            "⭐ Выберите стиль (по умолчанию без стиля):",
            reply_markup=kb.style_button
        )

    elif callback.data in list.styles:
        user_id = g.get_user_id(callback)
        if callback.data == "no_style":
            value = " "

        else:
            value = str(callback.data)
        df.add_style_to_user(user_id, value.split())
        await callback.message.edit_text(
            "*✅ Стиль успешно применён.* \nВы можете продолжить настраивать параметры, или начать генерацию.",
            reply_markup=kb.params_menu,
            parse_mode="Markdown"
        )

    elif callback.data == "cfg_scale":
        await callback.message.edit_text(
            "📊 Выберите значение CFG (по умолчанию 7.0, советуем не выставлять слишком высокие значения):",
            reply_markup=kb.cfg_scale_button
        )

    elif callback.data in list.cfg_scale:
        user_id = g.get_user_id(callback)
        param = "cfg_scale"
        value = callback.data
        df.add_argument_to_user(user_id, param, float(value))
        await callback.message.edit_text(
            "✅ Успешно. \nВы можете продолжить настраивать параметры, или начать генерацию.",
            reply_markup=kb.params_menu
        )

    elif callback.data == "set_default":
        user_id = g.get_user_id(callback)
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

    elif callback.data in list.models:
        user_id = g.get_user_id(callback)
        if callback.data == "midj":
            value = "ANYTHING_MIDJOURNEY_V_4.1.ckpt [041eabfcc6]"
            df.set_model_to_user(user_id, value)
        elif callback.data == "revAnim":
            value = "revAnimated_v122.safetensors [f8bb2922e1]"
            df.set_model_to_user(user_id, value)

        elif callback.data == "pruned":
            value = "v1-5-pruned.ckpt [e1441589a6]"
            df.set_model_to_user(user_id, value)

        elif callback.data == "deliberate":
            value = "deliberate_v2.safetensors [9aba26abdf]"
            df.set_model_to_user(user_id, value)

        await callback.message.edit_text(
            "*✅ Успешно. *\nВы можете продолжить настраивать параметры, или начать генерацию.",
            reply_markup=kb.params_menu,
            parse_mode="Markdown"
        )

    elif callback.data == "negative_prompt":
        await callback.message.edit_text(
            "Отправьте негативный запрос: ",
            reply_markup=kb.back_button
        )
        await Form.text.set()

    elif callback.data == "format":
        await callback.message.edit_text(
            "Выберите формат изображения: ",
            reply_markup=kb.format_menu
        )

    elif callback.data in list.formats:
        user_id = g.get_user_id(callback)
        format = int(callback.data)
        param = "width"
        df.add_argument_to_user(user_id, param, format)
        await callback.message.edit_text(
            "*✅ Успешно. *\nВы можете продолжить настраивать параметры, или начать генерацию.",
            reply_markup=kb.params_menu,
            parse_mode="Markdown"
        )


    elif callback.data == "resume":
        info = df.get_info_for_render(g.get_user_id(callback))
        await callback.message.edit_text(
            info,
            reply_markup=kb.start_render,
            parse_mode="Markdown"
        )

    elif callback.data == "start_render":
        await callback.message.delete()
        msg = await bot.send_sticker(
            callback.from_user.id,
            t.sticker
        )
        user_id = g.get_user_id(callback)
        photo = sd.render_photo(user_id)
        await msg.delete()
        await bot.send_photo(
            callback.from_user.id,
            photo,
            reply_markup=kb.regenerate_photo_button
        )

    elif callback.data == "repeat":
        msg = await bot.send_sticker(
            callback.from_user.id,
            t.sticker
        )
        user_id = g.get_user_id(callback)
        photo = sd.render_photo(user_id)
        await msg.delete()
        await bot.send_photo(
            callback.from_user.id,
            photo,
            reply_markup=kb.regenerate_photo_button
        )


@dp.message_handler(state=Form.text)
async def process_text(message: types.Message, state: FSMContext):
    user_id = g.get_user_id(message)
    no_translated_negative_prompt = message.text
    if len(no_translated_negative_prompt) > 1500:
        await message.reply(
            "*❌ Негативный запрос слишком большой. *\n"
             "Максимальная длина негативного запроса *1700* символов.",
            parse_mode="Markdown"
        )
    else:
        negative_prompt = tr.translate(no_translated_negative_prompt)
        df.add_negative_prompt_to_user(user_id, negative_prompt)
        await message.reply(
            "*✅ Негативный запрос был успешно применён.*"
            "\nВы можете продолжить настраивать параметры, или начать генерацию.",
            reply_markup=kb.params_menu,
            parse_mode="Markdown"
        )
        await state.finish()


@dp.message_handler(content_types=['text'])
async def generate_photo(message: types.Message):
    no_translated_prompt = message.text
    if len(no_translated_prompt) > 1700:
        await bot.send_message(
            message.chat.id,
            "*❌ Ваш запрос слишком большой. *\n"
            "Максимальная длина запроса *1700* символов.",
            parse_mode="Markdown"
        )
    else:
        try:
            prompt = tr.translate(no_translated_prompt)
            df.add_prompt_to_user(g.get_user_id(message), prompt)
            await bot.send_message(
                message.chat.id,
                t.main_menu_message,
                reply_markup=kb.params_menu)
        # На случай если сайт не ответит
        except requests.RequestException:
            await bot.send_message(
                message.chat.id,
                "❌ При переводе запроса произошла ошибка, попробуйте ещё раз."
            )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)