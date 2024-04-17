from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router(name=__name__)


@router.message(Command(commands=['ref', 'referral']))
async def referral_info(message: Message):
    await message.answer('👥 Реферальная система:\n\n'
                         '❕ Независимо от количества рефералов за каждого выдаётся 10 минут PREMIUM\n\n'
                         '1️⃣ ступень:\n'
                         '5 рефералов = 1 час PREMIUM\n\n'
                         '2️⃣ ступень:\n'
                         '10 рефералов = 1 день PREMIUM\n\n'
                         '3️⃣ ступень:\n'
                         '20 рефералов = 2 дня PREMIUM')
