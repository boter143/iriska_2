from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tgbot.utils.const_functions import rkb


# Кнопки главного меню
def menu_frep() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb('👤 Профиль')
    )

    keyboard.row(
        rkb('⚡️ PREMIUM'),
        rkb('🗂 Архив')
    )

    keyboard.row(
        rkb('ℹ️ Информация')
    )

    keyboard.row(
        rkb('📹 Отправить видео')
    )

    return keyboard.as_markup(resize_keyboard=True)


# Кнопка после отправки
def send_video_frep() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb('✔️ Остановить')
    )

    return keyboard.as_markup(resize_keyboard=True)
