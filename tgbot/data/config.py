from environs import Env
from platform import python_version

env = Env()
env.read_env()

# .env
BOT_TOKEN = env.str('BOT_TOKEN')
ADMIN_ID = env.int('ADMIN_ID')
DISCORD_LINK = env.str('DISCORD_LINK')
CHAT_ID = env.int('CHAT_ID')
PAY_API = env.str('PAY_API')
PAY_SECRET = env.str('PAY_SECRET')
PAY_MERCHANT_ID = env.str('PAY_MERCHANT_ID')
MINUTES_PER_REFERRAL = env.int('MINUTES_PER_REFERRAL')
MINUTES_PER_VIDEO = env.int('MINUTES_PER_VIDEO')

# consts
PY_VERSION = python_version()
BOT_TIMEZONE = "Europe/Moscow"  # Временная зона бота

# PATHS
PATH_DATABASE = "tgbot/data/database.db"
