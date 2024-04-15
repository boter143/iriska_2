from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from tgbot.database.db_users import Userx
from tgbot.data.config import ADMIN_ID
from tgbot.keyboards.inline_main import admin_answer_finl

router = Router(name=__name__)


class UserHelp(StatesGroup):
    help = State()


@router.message(Command(commands=['help']))
async def user_help(message: Message, state: FSMContext):
    await message.answer(f'<b>🆘 Помощь</b>\n\n'
                         f'Постарайтесь как можно подробнее описать вашу проблему!\n\n'
                         f'Медиа, голосовые, повторные сообщения не принимаются\n\n'
                         f'<b>ЗА СПАМ МОМЕНТАЛЬНЫЙ БАН, ОЖИДАЙТЕ ОТВЕТА В ТЕЧЕНИЕ 24 ЧАСОВ!</b>\n'
                         f'Для отмены отправьте строго: 0')

    await state.set_state(UserHelp.help)


@router.message(UserHelp.help)
async def send_help(message: Message, bot: Bot, state: FSMContext):
    if message.text == "0":
        return

    await message.answer('✅ Ваше сообщение успешно отправлено!\n'
                         'Ожидайте ответа!')

    user = Userx.get(user_id=message.from_user.id)

    # Проверка на бан
    if user.user_ban == 0:
        user_ban = '✅ Не забанен'
    elif user.user_ban == 1:
        user_ban = '⛔️ Забанен'

    try:
        await bot.send_message(chat_id=ADMIN_ID, text=f'🆘 #Помощь\n\n'
                                                      f'🆔: <code>{user.user_id}</code>\n'
                                                      f'{user_ban}\n\n'
                                                      f'Сообщение: {message.text}', reply_markup=admin_answer_finl())
    except:
        pass

    await state.clear()
