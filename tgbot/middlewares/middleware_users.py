from aiogram import BaseMiddleware
from aiogram.types import User

from tgbot.database.db_users import Userx


# Проверка юзера в БД и его добавление
class ExistsUserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        this_user: User = data.get("event_from_user")

        if not this_user.is_bot:
            get_user = Userx.get(user_id=this_user.id)

            user_id = this_user.id

            if get_user is None:
                Userx.add(user_id)

        return await handler(event, data)
