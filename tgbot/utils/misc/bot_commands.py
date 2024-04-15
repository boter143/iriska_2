from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat

from tgbot.data.config import ADMIN_ID

# Users команды
user_commands = [
    BotCommand(command='start', description='♻️ Перезапустить бота'),
    BotCommand(command='help', description='🆘 Помощь'),
]

# Admin команды
admin_commands = [
    BotCommand(command='start', description='♻️ Перезапустить бота'),
    BotCommand(command='help', description='🆘 Помощь'),
    BotCommand(command='admin', description='👑 Админ-панель'),
    BotCommand(command='db', description='📦 Получить Базу Данных'),
]


# Установка комманд
async def set_commands(bot: Bot):
    await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())

    try:
        await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=ADMIN_ID))
    except ValueError:
        pass
