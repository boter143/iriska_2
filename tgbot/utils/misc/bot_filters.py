from typing import Union

from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from tgbot.data.config import ADMIN_ID


class IsAdmin(BaseFilter):
    async def __call__(self, update: Union[Message, CallbackQuery], bot: Bot):
        if update.from_user.id == ADMIN_ID:
            return True
        else:
            return False
