from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Command

start_menu = InlineKeyboardMarkup(row_width=1)
start_menu.add(
    InlineKeyboardButton(text="🎆 Получить пример", callback_data="get_example"),
    InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")
)

params_menu = InlineKeyboardMarkup(row_width=2)
params_menu.add(
    InlineKeyboardButton(text="🌌 Метод отбора", callback_data="sampling_method"),
    InlineKeyboardButton(text="⭐ Стили", callback_data="styles"),
    InlineKeyboardButton(text="🥇 Шаги выборки", callback_data="sampling_steps"),
    InlineKeyboardButton(text="📊 Шкала CFG", callback_data="cfg_scale"),
    InlineKeyboardButton(text="🛠 Установить параметры по умолчанию", callback_data="set_default"),
    InlineKeyboardButton(text="🤖 Модель", callback_data="model"),
    InlineKeyboardButton(text="➡️ Продолжить", callback_data="resume")
)

sampling_method_menu = InlineKeyboardMarkup(row_width=3)
sampling_method_menu.add(
    InlineKeyboardButton(text="Euler a", callback_data="Euler a"),
    InlineKeyboardButton(text="Euler", callback_data="Euler"),
    InlineKeyboardButton(text="LMS", callback_data="LMS"),
    InlineKeyboardButton(text="DPM2", callback_data="DPM2"),
    InlineKeyboardButton(text="DPM adaptive", callback_data="DPM adaptive"),
    InlineKeyboardButton(text="DDIM", callback_data="DDIM")
)


cfg_scale_button = InlineKeyboardMarkup(row_width=3)
cfg_scale_button.add(
    InlineKeyboardButton(text="1.0", callback_data="1.0"),
    InlineKeyboardButton(text="3.0", callback_data="3.0"),
    InlineKeyboardButton(text="5.0", callback_data="5.0"),
    InlineKeyboardButton(text="7.0", callback_data="7.0"),
    InlineKeyboardButton(text="9.0", callback_data="9.0"),
    InlineKeyboardButton(text="11.0", callback_data="11.0"),
    InlineKeyboardButton(text="13.0", callback_data="13.0"),
    InlineKeyboardButton(text="15.0", callback_data="15.0"),
    InlineKeyboardButton(text="20.0", callback_data="20.0"),
    InlineKeyboardButton(text="25.0", callback_data="25.0"),
    InlineKeyboardButton(text="30.0", callback_data="30.0"),
    InlineKeyboardButton(text="40.0", callback_data="40.0"),
)


sampling_steps_button = InlineKeyboardMarkup(row_width=3)
sampling_steps_button.add(
    InlineKeyboardButton(text="10", callback_data="10"),
    InlineKeyboardButton(text="13", callback_data="13"),
    InlineKeyboardButton(text="15", callback_data="15"),
    InlineKeyboardButton(text="20", callback_data="20"),
    InlineKeyboardButton(text="23", callback_data="23"),
    InlineKeyboardButton(text="25", callback_data="25"),
    InlineKeyboardButton(text="30", callback_data="30"),
    InlineKeyboardButton(text="35", callback_data="35"),
    InlineKeyboardButton(text="40", callback_data="40"),
    InlineKeyboardButton(text="45", callback_data="45"),
    InlineKeyboardButton(text="50", callback_data="50"),
    InlineKeyboardButton(text="55", callback_data="55"),
)


style_button = InlineKeyboardMarkup(row_width=2)
style_button.add(
    InlineKeyboardButton(text="Аниме", callback_data="Anime"),
    InlineKeyboardButton(text="Манга", callback_data="Manga"),
    InlineKeyboardButton(text="Фото", callback_data="Photo"),
    InlineKeyboardButton(text="Пиксель-арт", callback_data="Pixel art"),
    InlineKeyboardButton(text="Киберпанк", callback_data="Cyberpunk"),
    InlineKeyboardButton(text="Скетч", callback_data="Sketch"),
    InlineKeyboardButton(text="Гладкое лицо", callback_data="SmoothFace"),
    InlineKeyboardButton(text="Макросьёмка", callback_data="Macro-Photo"),
    InlineKeyboardButton(text="Фэнтези", callback_data="Fantasy"),
    InlineKeyboardButton(text="Без стиля", callback_data="no_style"),
    InlineKeyboardButton(text="⬅️ Назад", callback_data="back_in_menu")
)

start_generation_button = InlineKeyboardMarkup(row_width=1)
start_generation_button.add(
    InlineKeyboardButton(text="🚀 Начать генерацию", callback_data="start_generation"),
)

models_menu = InlineKeyboardMarkup(row_width=1)
models_menu.add(
    InlineKeyboardButton(text="🏞 ANYTHING MIDJ v1.0", callback_data="midj"),
    InlineKeyboardButton(text="🌄 RevAnimated v1.22 (🆕 BEST)", callback_data="revAnim"),
)
