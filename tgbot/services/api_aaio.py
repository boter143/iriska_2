import asyncio

from AaioAPI import AsyncAaioAPI
from aiogram import Bot

from tgbot.database.db_users import Userx
from tgbot.data.config import PAY_API, PAY_SECRET, PAY_MERCHANT_ID

client = AsyncAaioAPI(
    API_KEY=PAY_API,
    SECRET_KEY=PAY_SECRET,
    MERCHANT_ID=PAY_MERCHANT_ID)


async def create_pay_link(amount, order_id):
    amount = amount  # Сумма к оплате
    currency = 'RUB'  # Валюта заказа
    order_id = order_id  # Идентификатор заказа в Вашей системе
    desc = 'Покупка berrycoins'  # Описание заказа
    lang = 'ru'  # Язык формы

    url_to_pay = await client.create_payment(order_id, amount, lang, currency, desc)

    return url_to_pay


async def check_status(user_id, order_id, amount, bot: Bot):
    while True:
        try:
            if await client.is_expired(order_id):  # если счёт просрочен
                break
            elif await client.is_success(order_id):  # если оплата прошла успешно
                Userx.user_change_balance(user_id=user_id, count=amount)
                try:
                    await bot.send_message(chat_id=user_id, text=f'ID заказа: {order_id}\n\n'
                                                                 f'✅ Успешная оплата!')
                except:
                    pass
                break
        except:
            pass
        await asyncio.sleep(10)
