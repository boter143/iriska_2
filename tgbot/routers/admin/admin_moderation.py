from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from tgbot.database.db_users import Userx
from tgbot.database.db_video import Videox
from tgbot.keyboards.inline_main import admin_moderation_finl
from tgbot.keyboards.reply_main import send_video_frep, menu_frep
from tgbot.data.config import CHAT_ID

router = Router(name=__name__)


class AdminModeration(StatesGroup):
    in_moderation = State()
    stop_moderation = State()


# Обработка запроса на модерацию видео
@router.callback_query(F.data == 'admin_moderation_video')
async def start_admin_moderation(call: CallbackQuery, bot: Bot, state: FSMContext):
    try:
        all_video_id = Videox.get_all_id()
    except:
        await call.answer('⚠️ Ошибка!')

    video_index = 0

    try:
        video = Videox.get(video_id=all_video_id[video_index][0])

        if video.video_check == 1:
            while video.video_check == 1:
                video_index += 1
                video = Videox.get(video_id=all_video_id[video_index][0])

        await state.update_data(video_index=video_index + 1)
        await call.message.answer('⚠️ Если захочешь остановиться, нажми кнопку снизу!', reply_markup=send_video_frep())
    except:
        await call.message.answer('⚠️ Нет видео для модерации!', reply_markup=menu_frep())
        await state.clear()
        return

    try:
        await bot.copy_message(from_chat_id=CHAT_ID, chat_id=call.message.chat.id, message_id=video.video_id,
                               reply_markup=admin_moderation_finl())
    except:
        pass


# Обработка подтверждения видео
@router.callback_query(F.data == 'moderation_access')
async def admin_moderation_access(call: CallbackQuery, bot: Bot, state: FSMContext):
    state_data = await state.get_data()
    await call.message.delete()

    try:
        video_index = state_data['video_index']
        all_video_id = Videox.get_all_id()
    except:
        await call.answer('⚠️ Ошибка!')

    try:
        last_video = Videox.get(video_id=all_video_id[video_index - 1][0])
        if last_video.video_check == 0:
            Videox.video_change_status(video_id=all_video_id[video_index - 1][0])
    except:
        pass

    try:
        video = Videox.get(video_id=all_video_id[video_index][0])

        if video.video_check == 1:
            while video.video_check == 1:
                video_index += 1
                video = Videox.get(video_id=all_video_id[video_index][0])

        await state.update_data(video_index=video_index + 1)
    except:
        await call.message.answer('⚠️ Нет видео для модерации!', reply_markup=menu_frep())
        await state.clear()
        return

    try:
        await bot.copy_message(from_chat_id=CHAT_ID, chat_id=call.message.chat.id, message_id=video.video_id,
                               reply_markup=admin_moderation_finl())
    except:
        pass


# Обработка предупреждения пользователю на видео
@router.callback_query(F.data == 'moderation_warn')
async def admin_moderation_ban(call: CallbackQuery, bot: Bot, state: FSMContext):
    state_data = await state.get_data()
    await call.message.delete()

    try:
        video_index = state_data['video_index']
        all_video_id = Videox.get_all_id()
    except:
        await call.answer('⚠️ Ошибка!')
        return

    try:
        video_ban = Videox.get(video_id=all_video_id[video_index - 1][0])
    except:
        pass

    # Удаление видео везде
    try:
        # ОБРАБОТКА ВЫДАЧИ ПРЕДУПРЕЖДЕНИЯ/БАНА ПОЛЬЗОВАТЕЛЮ!
        user_video_ban = Userx.get(user_id=video_ban.user_id)

        if user_video_ban.user_warnings < 3:
            try:
                await bot.send_message(chat_id=user_video_ban.user_id,
                                       text=f'❗️ Вам было выдано предупреждение {user_video_ban.user_warnings + 1}/3\n'
                                            f'<b>Причина:</b> Нарушение правил.')
            except:
                pass
            Userx.user_add_warning(user_id=user_video_ban.user_id, warnings=user_video_ban.user_warnings)
        else:
            user_video_ban_id = user_video_ban.user_id
            if Userx.get(user_id=user_video_ban_id).user_ban == 0:
                Userx.user_ban_unban(user_video_ban_id)
                await call.message.answer(
                    f'⛔ Пользователь {user_video_ban_id} был <b>забанен</b>!\n'
                    f'☑️ Видео {video_ban.video_id} было удалено!')
                try:
                    await bot.send_message(chat_id=user_video_ban_id, text='⛔ Вы были забанены администратором!\n'
                                                                           'Теперь Вы не сможете отправлять видео\n\n'
                                                                           '<b>Причина:</b> Было отправлено более 3 некорректных видео.')
                except:
                    pass
            else:
                await call.message.answer(f'⛔ Пользователь {user_video_ban_id} уже забанен!\n'
                                          f'☑️ Видео {video_ban.video_id} было удалено!')

        Userx.user_uptime(user_id=user_video_ban.user_id, minutes=-3)
        Videox.video_delete(video_ban.video_id)
        await bot.delete_message(chat_id=CHAT_ID, message_id=video_ban.video_id)
        await call.message.answer(f'☑️ Видео {video_ban.video_id} было удалено!')

    except ValueError:
        await call.message.answer('⚠️ Некорректный id видео!\n')

    try:
        video = Videox.get(video_id=all_video_id[video_index][0])
        await state.update_data(video_index=video_index)
    except:
        await call.message.answer('⚠️ Нет видео для модерации!', reply_markup=menu_frep())
        await state.clear()
        return

    try:
        await bot.copy_message(from_chat_id=CHAT_ID, chat_id=call.message.chat.id, message_id=video.video_id,
                               reply_markup=admin_moderation_finl())
    except:
        pass


# Удаление видео
@router.callback_query(F.data == 'moderation_delete')
async def admin_moderation_ban(call: CallbackQuery, bot: Bot, state: FSMContext):
    state_data = await state.get_data()
    await call.message.delete()

    try:
        video_index = state_data['video_index']
        all_video_id = Videox.get_all_id()
    except:
        await call.answer('⚠️ Ошибка!')
        return

    try:
        video_ban = Videox.get(video_id=all_video_id[video_index - 1][0])
    except:
        pass

    user_video_ban = video_ban.user_id

    # Удаление видео везде
    try:
        Userx.user_uptime(user_id=user_video_ban, minutes=-3)
        Videox.video_delete(video_ban.video_id)
        await bot.delete_message(chat_id=CHAT_ID, message_id=video_ban.video_id)
        await call.message.answer(f'☑️ Видео {video_ban.video_id} было удалено!')
    except ValueError:
        await call.message.answer('⚠️ Некорректный id видео!\n')

    try:
        video = Videox.get(video_id=all_video_id[video_index][0])
        await state.update_data(video_index=video_index)
    except:
        await call.message.answer('⚠️ Нет видео для модерации!', reply_markup=menu_frep())
        await state.clear()
        return

    try:
        await bot.copy_message(from_chat_id=CHAT_ID, chat_id=call.message.chat.id, message_id=video.video_id,
                               reply_markup=admin_moderation_finl())
    except:
        pass


# Обработка бана юзера с некорректным видео
@router.callback_query(F.data == 'moderation_ban')
async def admin_moderation_ban(call: CallbackQuery, bot: Bot, state: FSMContext):
    state_data = await state.get_data()
    await call.message.delete()

    try:
        video_index = state_data['video_index']
        all_video_id = Videox.get_all_id()
    except:
        await call.answer('⚠️ Ошибка!')
        return

    try:
        video_ban = Videox.get(video_id=all_video_id[video_index - 1][0])
    except:
        pass

    try:
        # Удаление видео везде
        Videox.video_delete(video_ban.video_id)
        await bot.delete_message(chat_id=CHAT_ID, message_id=video_ban.video_id)

        # Бан пользователя
        user_to_ban = video_ban.user_id
        if Userx.get(user_id=user_to_ban).user_ban == 0:
            Userx.user_ban_unban(user_to_ban)
            await call.message.answer(
                f'⛔ Пользователь {user_to_ban} был <b>забанен</b>!\n'
                f'☑️ Видео {video_ban.video_id} было удалено!')
            try:
                await bot.send_message(chat_id=user_to_ban, text='⛔ Вы были забанены администратором!\n'
                                                                 'Теперь Вы не сможете отправлять видео\n\n'
                                                                 '<b>Причина:</b> Было отправлено не корректное видео.')
            except:
                pass
        else:
            await call.message.answer(f'⛔ Пользователь {user_to_ban} уже забанен!\n'
                                      f'☑️ Видео {video_ban.video_id} было удалено!')
    except:
        await call.message.answer('⚠️ Некорректный id пользователя!\n')

    try:
        video = Videox.get(video_id=all_video_id[video_index][0])
        await state.update_data(video_index=video_index)
    except:
        await call.message.answer('⚠️ Нет видео для модерации!', reply_markup=menu_frep())
        await state.clear()
        return

    try:
        await bot.copy_message(from_chat_id=CHAT_ID, chat_id=call.message.chat.id, message_id=video.video_id,
                               reply_markup=admin_moderation_finl())
    except:
        pass


# Обработка остановки
@router.message(F.text == '✔️ Остановить')
async def stop_moderation(message: Message):
    await message.answer('Модерация завершена!', reply_markup=menu_frep())
