from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.utils.const_functions import ikb
from tgbot.data.config import DISCORD_LINK


# Подписаться на discord
def discord_link_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Подписаться", url=DISCORD_LINK)
    )

    return keyboard.as_markup()


# Кнопки для админ панели
def admin_panel_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("🛠 Модерация видео", data='admin_moderation_video')
    )

    keyboard.row(
        ikb("👤 Пользователь", data='admin_user')
    )

    keyboard.row(
        ikb("📢 Рассылка", data='admin_mailing')
    )

    return keyboard.as_markup()


# Кнопки для админ панели
def admin_mailing_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Подтвердить", data='admin_mailing_true'),
        ikb("📝 Изменить", data='admin_mailing_false')
    )

    keyboard.row(
        ikb("📢 Отменить", data='admin_mailing_cancel')
    )

    return keyboard.as_markup()


# Кнопки для манипуляции пользователем
def admin_user_finl(ban_btn) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("💰 Добавить / Убавить", data='admin_change_balance')
    )

    keyboard.row(
        ikb(ban_btn, data='admin_ban_unban_user'),
        ikb("⏰ Время", data='admin_change_time')
    )

    return keyboard.as_markup()


# Кнопки под видео-модерацию
def admin_moderation_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Принять", data='moderation_access'),
        ikb("❌️Удалить", data='moderation_delete')
    )

    keyboard.row(
        ikb("⚠️ Предупреждение", data='moderation_warn'),
        ikb("⛔️ Забанить", data='moderation_ban')
    )

    return keyboard.as_markup()


# Оплата
def balance_add_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("Пополнить баланс", data='balance_add')
    )

    return keyboard.as_markup()


# Способы оплаты
def pay_method_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("💳 Карта (РФ, Украина, Казахстан)", data='pay_aaio')
    )

    keyboard.row(
        ikb("🪙 Крипта", data='pay_aaio')
    )

    return keyboard.as_markup()


def admin_answer_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("Ответить", data='admin_answer')
    )

    return keyboard.as_markup()


# Ссылка на оплату
def pay_link_finl(link) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("💵 Оплатить", url=link)
    )

    return keyboard.as_markup()


# Тарифы VIP
def premium_tariffs() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("3 дня - 300 berrycoins", data="3days_premium")
    )

    keyboard.row(
        ikb("7 дней - 600 berrycoins", data="7days_premium")
    )

    keyboard.row(
        ikb("14 дней - 1000 berrycoins", data="14days_premium")
    )

    return keyboard.as_markup()


# Тарифы архив
def archive_tariffs() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("100 видео - 200 berrycoins", data="100_archive")
    )

    keyboard.row(
        ikb("300 видео - 500 berrycoins", data="300_archive")
    )

    keyboard.row(
        ikb("700 видео - 1000 berrycoins", data="700_archive")
    )

    return keyboard.as_markup()

#
