import re

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router(name=__name__)


class AdminAnswer(StatesGroup):
    answer = State()


# Обработка запроса пользователя
@router.callback_query(F.data == 'admin_answer')
async def admin_answer(call: CallbackQuery, state: FSMContext):
    message = call.message.text

    id_pattern = r'🆔: (\d+)'

    match = re.search(id_pattern, message)

    if match:
        # Получение найденного ID
        user_id = match.group(1)
    else:
        await call.message.answer("ID не найден")

    await state.update_data(user_id=user_id)

    await call.message.answer('❕ Введите ответ на вопрос:')

    await state.set_state(AdminAnswer.answer)


# Ответ пользователю на запрос
@router.message(AdminAnswer.answer)
async def send_answer(message: Message, bot: Bot, state: FSMContext):
    state_data = await state.get_data()
    user_id = state_data['user_id']

    try:
        await bot.send_message(chat_id=user_id, text='❗️АДМИНИСТРАТОР ОТВЕТИЛ ВАМ❗️\n\n'
                                                     f'Ответ: {message.text}')
        await message.answer(f'✅ Сообщение пользователю {user_id} успешно отправлено!')
    except:
        await message.answer(f'🚫 Ошибка отправки сообщения пользователю {user_id}!')

    await state.clear()
