import pytz, time

from aiogram.types import KeyboardButton, InlineKeyboardButton
from datetime import datetime
from typing import Union

from tgbot.data.config import BOT_TIMEZONE


#################################### AIOGRAM ####################################

# Генерация reply кнопки
def rkb(text: str) -> KeyboardButton:
    return KeyboardButton(text=text)


# Генерация inline кнопки
def ikb(text: str, data: str = None, url: str = None) -> InlineKeyboardButton:
    if data is not None:
        return InlineKeyboardButton(text=text, callback_data=data)
    elif url is not None:
        return InlineKeyboardButton(text=text, url=url)


#################################### ПРОЧЕЕ ####################################

# Получение даты
def get_date(full: bool = True) -> str:
    if full:  # Полная дата с временем
        return datetime.now(pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y %H:%M:%S")
    else:  # Только дата без времени
        return datetime.now(pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y")


# Получение unix времени
def get_unix(full: bool = False) -> int:
    if full:  # Получение времени в наносекундах
        return time.time_ns()
    else:  # Получение времени в секундах
        return int(time.time())


# Удаление отступов у текста
def ded(get_text: str) -> str:
    if get_text is not None:
        split_text = get_text.split("\n")

        if split_text[0] == "": split_text.pop(0)
        if split_text[-1] == "": split_text.pop()
        save_text = []

        for text in split_text:
            while text.startswith(" "):
                text = text[1:]

            save_text.append(text)
        get_text = "\n".join(save_text)
    else:
        get_text = ""

    return get_text


# Конвертация unix в дату и даты в unix
def convert_date(from_time, full=True, second=True) -> Union[str, int]:
    from tgbot.data.config import BOT_TIMEZONE

    if "-" in str(from_time):
        from_time = from_time.replace("-", ".")

    if str(from_time).isdigit():
        if full:
            to_time = datetime.fromtimestamp(from_time, pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y %H:%M:%S")
        elif second:
            to_time = datetime.fromtimestamp(from_time, pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y %H:%M")
        else:
            to_time = datetime.fromtimestamp(from_time, pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y")
    else:
        if " " in str(from_time):
            cache_time = from_time.split(" ")

            if ":" in cache_time[0]:
                cache_date = cache_time[1].split(".")
                cache_time = cache_time[0].split(":")
            else:
                cache_date = cache_time[0].split(".")
                cache_time = cache_time[1].split(":")

            if len(cache_date[0]) == 4:
                x_year, x_month, x_day = cache_date[0], cache_date[1], cache_date[2]
            else:
                x_year, x_month, x_day = cache_date[2], cache_date[1], cache_date[0]

            x_hour, x_minute, x_second = cache_time[0], cache_time[2], cache_time[2]

            from_time = f"{x_day}.{x_month}.{x_year} {x_hour}:{x_minute}:{x_second}"
        else:
            cache_date = from_time.split(".")

            if len(cache_date[0]) == 4:
                x_year, x_month, x_day = cache_date[0], cache_date[1], cache_date[2]
            else:
                x_year, x_month, x_day = cache_date[2], cache_date[1], cache_date[0]

            from_time = f"{x_day}.{x_month}.{x_year}"

        if " " in str(from_time):
            to_time = int(datetime.strptime(from_time, "%d.%m.%Y %H:%M:%S").timestamp())
        else:
            to_time = int(datetime.strptime(from_time, "%d.%m.%Y").timestamp())

    return to_time
