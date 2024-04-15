import asyncio

from random import randint

from aiogram import Bot

from tgbot.database.db_users import Userx
from tgbot.database.db_video import Videox
from tgbot.data.config import CHAT_ID

# Бесконечная отправка видео всем, у кого есть доступ
from tgbot.utils.const_functions import get_unix


async def send_archive_video_to_all(bot: Bot):
    index = 0
    list_off = False

    while True:
        try:
            all_users_id = Userx.get_all_id()
            videos_id = Videox.get_all_id()
        except:
            pass

        try:
            videos_id[index][0]
        except:
            list_off = True

        if not list_off:
            for user_id in all_users_id:
                user_id = user_id[0]

                if Userx.get(user_id=user_id).user_unix > get_unix():
                    try:
                        await bot.copy_message(from_chat_id=CHAT_ID, chat_id=user_id, message_id=videos_id[index][0],
                                               protect_content=True)
                    except:
                        pass

        if list_off:
            index = 0
            list_off = False
        else:
            index += 1

        await asyncio.sleep(randint(40, 80))


async def send_archive_video_to_user(user_id, amount, index, bot: Bot):
    index = index
    trys = 0

    while trys < amount:
        try:
            videos_id = Videox.get_all_id()
        except:
            pass

        try:
            await bot.copy_message(from_chat_id=CHAT_ID, chat_id=user_id, message_id=videos_id[index][0])
            index += 1
        except:
            index += 1

        trys += 1
        await asyncio.sleep(randint(3, 10))

    await bot.send_message(chat_id=user_id, text=f'✅ Было переслано {amount} видео')

    Userx.user_change_index_video(user_id=user_id, count=amount)
