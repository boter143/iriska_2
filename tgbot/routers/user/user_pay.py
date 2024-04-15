import uuid

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from tgbot.keyboards.inline_main import pay_method_finl, pay_link_finl
from tgbot.utils.const_functions import convert_date, get_unix
from tgbot.services.api_aaio import create_pay_link, check_status

router = Router(name=__name__)


class UserPay(StatesGroup):
    pay_aaio = State()


# Выбор способа оплаты
@router.callback_query(F.data == 'balance_add')
async def add_balance(call: CallbackQuery):
    await call.message.answer('Выберите способ оплаты:', reply_markup=pay_method_finl())


# Количество berrycoins для пополнение в aaio
@router.callback_query(F.data == 'pay_aaio')
async def pay_aaio(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Введите количество berrycoins\n'
                              '(минимум 100) для пополнения')
    await state.set_state(UserPay.pay_aaio)


# Обработка платежа, создание ссылки
@router.message(UserPay.pay_aaio)
async def display_link(message: Message, bot: Bot, state: FSMContext):
    await message.delete()
    if not message.text.isdigit() or int(message.text) < 100:
        await message.answer('<b>Пожалуйста, укажите число больше 100</b>\n'
                             'Пример: 1000')
        await state.set_state(UserPay.pay_aaio)
        return

    amount = int(message.text)
    order_id = uuid.uuid4()

    url = await create_pay_link(amount=amount, order_id=order_id)

    await message.answer(f'ID оплаты:\n<code>{order_id}</code>\n\n'
                         f'Сумма пополнения: {message.text} berrycoins\n\n'
                         f'До: {convert_date(get_unix() + 60 * 60 * 6, False)}',
                         reply_markup=pay_link_finl(link=url))

    await state.clear()
    await check_status(message.from_user.id, order_id, amount, bot)
