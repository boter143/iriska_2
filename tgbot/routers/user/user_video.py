from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from tgbot.database.db_users import Userx
from tgbot.database.db_video import Videox
from tgbot.keyboards.reply_main import send_video_frep, menu_frep
from tgbot.data.config import CHAT_ID, MINUTES_PER_VIDEO

router = Router(name=__name__)


class sendVideo(StatesGroup):
    take_message = State()


# Запуск приёмщика видео
@router.message(F.text == '📹 Отправить видео')
async def about_video(message: Message, state: FSMContext):
    await message.answer('⚠️ Можно отправлять 2 видео одним сообщением\n\n'
                         'Если хотите остановиться, нажмите на кнопку снизу',
                         reply_markup=send_video_frep())

    await state.update_data(count_video='0')
    await state.update_data(count_unic_video=0)

    await state.set_state(sendVideo.take_message)


# Обработка отправленного сообщения в приёмщик
@router.message(sendVideo.take_message)
async def filter_video(message: Message, state: FSMContext, bot: Bot):
    user = Userx.get(user_id=int(message.from_user.id))
    if message.video and user.user_ban != 1:
        state_data = await state.get_data()

        # Данные о видео
        video_name = message.video.file_name
        video_size = message.video.file_size
        video_duration = message.video.duration

        # Изменение количества присланных видео
        try:
            new_count_video = int(state_data['count_video']) + 1
        except:
            return

        await state.update_data(count_video=new_count_video)

        # Проверка на уникальность видео
        if Videox.video_unic(video_name=video_name, video_size=video_size, video_duration=video_duration):
            # Счётчик уникальных видео
            new_count_unic_video = int(state_data['count_unic_video']) + 1
            await state.update_data(count_unic_video=new_count_unic_video)

            # Пересылка видео в тгк
            try:
                channel_message_copy = await bot.copy_message(from_chat_id=message.from_user.id, chat_id=CHAT_ID,
                                                              message_id=message.message_id)
                channel_message_id = int(channel_message_copy.message_id)
                await bot.edit_message_caption(chat_id=CHAT_ID, message_id=channel_message_id, caption=None)
            except:
                pass

            # Добавление видео в дб
            try:
                Videox.add(video_id=channel_message_id, video_name=video_name, video_size=video_size,
                           video_duration=video_duration, user_id=message.from_user.id)
            except:
                pass

            await state.set_state(sendVideo.take_message)
    else:
        if message.text == '✔️ Остановить':
            state_data = await state.get_data()
            time_up = state_data['count_unic_video'] * MINUTES_PER_VIDEO
            Userx.user_uptime(message.from_user.id, time_up)
            await message.answer(f"Уникальных: {state_data['count_unic_video']}/{state_data['count_video']} видео\n\n"
                                 f"Добавлено: {time_up} минут доступа!",
                                 reply_markup=menu_frep())
            await state.clear()
            return
        elif user.user_ban == 1:
            await message.answer('⛔ Вы были забанены администратором!\n'
                                 'Вы не можете отправлять видео')
        else:
            await message.answer('⚠ Не верный формат сообщения!')
            await state.set_state(sendVideo.take_message)
