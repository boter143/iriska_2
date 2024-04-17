from aiogram import Dispatcher, F

from tgbot.routers.user import user_menu, user_video, user_pay, user_help, user_referral
from tgbot.routers.admin import admin_menu, admin_moderation, admin_user, admin_help, admin_mailing
from tgbot.utils.misc.bot_filters import IsAdmin


def register_all_routers(dp: Dispatcher):
    # Подключение фильтров
    dp.message.filter(F.chat.type == "private")  # Работа бота только в личке - сообщения
    dp.callback_query.filter(F.message.chat.type == "private")  # Работа бота только в личке - колбэки

    admin_menu.router.message.filter(IsAdmin())
    admin_moderation.router.message.filter(IsAdmin())
    admin_moderation.router.callback_query.filter(IsAdmin())
    admin_user.router.message.filter(IsAdmin())
    admin_user.router.callback_query.filter(IsAdmin())
    admin_help.router.message.filter(IsAdmin())
    admin_help.router.callback_query.filter(IsAdmin())
    admin_mailing.router.message.filter(IsAdmin())
    admin_mailing.router.callback_query.filter(IsAdmin())

    # Подключение пользовательских роутеров (юзеров и админов)
    dp.include_router(user_video.router)  # user router
    dp.include_router(user_pay.router)  # user router
    dp.include_router(user_menu.router)  # user router
    dp.include_router(user_help.router)  # user router
    dp.include_router(user_referral.router)  # user router
    dp.include_router(admin_menu.router)  # admin router
    dp.include_router(admin_moderation.router)  # admin router
    dp.include_router(admin_user.router)  # admin router
    dp.include_router(admin_help.router)  # admin router
    dp.include_router(admin_mailing.router)  # admin router
