from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from tgbot.database.db_video import Videox
from tgbot.keyboards.inline_main import admin_panel_finl
from tgbot.database.db_users import Userx
from tgbot.data.config import PATH_DATABASE
from tgbot.utils.const_functions import get_date

router = Router(name=__name__)


# Админ-панель
@router.message(Command(commands=['admin']))
async def admin_menu(message: Message):
    try:
        video_avg = Videox.video_avg_all()
    except:
        video_avg = 0

    await message.answer(f'<b>👑 Админ-панель</b>\n\n'
                         f'Кол-во 👥: {Userx.get_all_count()}\n'
                         f'AVG 📹: {video_avg} сек',
                         reply_markup=admin_panel_finl())


# Бэк-ап db
@router.message(Command(commands=['db', 'database']))
async def admin_database(message: Message):
    await message.answer_document(
        FSInputFile(PATH_DATABASE),
        caption=f"<b>📦 #BACKUP | <code>{get_date()}</code></b>",
    )
