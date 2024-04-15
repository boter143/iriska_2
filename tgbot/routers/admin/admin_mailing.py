from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from tgbot.database.db_users import Userx
from tgbot.database.db_video import Videox
from tgbot.keyboards.inline_main import admin_moderation_finl, admin_mailing_finl
from tgbot.keyboards.reply_main import send_video_frep, menu_frep
from tgbot.data.config import CHAT_ID, ADMIN_ID

router = Router(name=__name__)


class AdminMailing(StatesGroup):
    check_mailing = State()


#####[ admin_mailing ]#####
@router.callback_query(F.data == 'admin_mailing')
async def admin_mailing(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('⚡️ Пришлите готовое сообщение прямо в чат!')

    await state.set_state(AdminMailing.check_mailing)


#####[ check_mailing ]#####
@router.message(AdminMailing.check_mailing)
async def check_mailing(message: Message, bot: Bot, state: FSMContext):
    await bot.copy_message(chat_id=ADMIN_ID, from_chat_id=message.from_user.id, message_id=message.message_id,
                           reply_markup=admin_mailing_finl())

    await message.delete()


#####[ admin_mailing_true ]#####
@router.callback_query(F.data == 'admin_mailing_true')
async def admin_mailing_true(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.message.edit_reply_markup()

    try:
        users_id = Userx.get_all_id()
    except:
        pass

    try:
        c = 0
        for user_id in users_id:
            try:
                await bot.copy_message(chat_id=user_id[0], from_chat_id=ADMIN_ID, message_id=call.message.message_id)
                c += 1
            except:
                pass
        await call.message.answer('✅ Рассылка была отправлена.\n'
                                  f'Получило: {c} пользователей')
    except:
        await call.message.answer('⚠️ Ошибка отправки рассылки')

    await call.message.delete()


#####[ admin_mailing_false ]#####
@router.callback_query(F.data == 'admin_mailing_false')
async def admin_mailing_false(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('⚡️ Пришлите готовое сообщение прямо в чат!')

    await state.set_state(AdminMailing.check_mailing)


#####[ admin_mailing_cancel ]#####
@router.callback_query(F.data == 'admin_mailing_cancel')
async def admin_mailing_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.delete()

    await call.message.answer('✅ Рассылка отменена!')

    await state.clear()
