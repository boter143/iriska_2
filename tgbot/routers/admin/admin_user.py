from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from tgbot.database.db_users import Userx
from tgbot.keyboards.inline_main import admin_user_finl

router = Router(name=__name__)


class AdminUser(StatesGroup):
    check_user_id = State()
    user_manipulation = State()
    user_change_balance = State()
    user_set_ban = State()
    user_change_time = State()


# Меню модерации над пользователем
@router.callback_query(F.data == 'admin_user')
async def admin_user(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Введите id пользователя: ')

    await state.set_state(AdminUser.check_user_id)


# Проверка на правильность id после его ввода
@router.message(AdminUser.check_user_id)
async def check_user_id(message: Message, bot: Bot, state: FSMContext):
    await message.delete()

    try:
        await bot.delete_message(chat_id=message.from_user.id, message_id=(message.message_id - 1))
    except:
        pass

    try:
        user_id = int(message.text)
    except:
        await state.clear()
        await message.answer('⚠️ Введёт некорректный id пользователя!\n'
                             'Попробуйте заново')
        return

    # Проверка id на подлинность
    try:
        if Userx.user_exist(user_id):
            await state.update_data(user_id=int(message.text))
            await state.set_state(AdminUser.user_manipulation)
    except:
        await state.clear()
        await message.answer(f'⚠️ Пользователя с id {user_id} не существует!\n'
                             f'Попробуйте заново!')
        return

    user = Userx.get(user_id=user_id)

    # Проверка на бан
    if user.user_ban == 0:
        user_ban = '✅ Не забанен'
        ban_btn = '⛔️ Забанить'
    elif user.user_ban == 1:
        user_ban = '⛔️ Забанен'
        ban_btn = '✅ Разбанить'

    await message.answer(f'👤 Пользователь: \n\n'
                         f'🆔: <code>{user.user_id}</code>\n'
                         f'💵: {user.user_balance}\n\n'
                         f'{user_ban}',
                         reply_markup=admin_user_finl(ban_btn))


##### [ USER_BALANCE ] #####
# Количество денег на добавление пользователю
@router.callback_query(F.data == 'admin_change_balance')
async def user_balance_to_change(call: CallbackQuery, state: FSMContext):
    await call.message.delete()

    await call.message.answer('Введите количество 💵, которое хотите добавить:')

    await state.set_state(AdminUser.user_change_balance)


# Изменения баланса пользователя
@router.message(AdminUser.user_change_balance)
async def check_user_id(message: Message, bot: Bot, state: FSMContext):
    await message.delete()

    try:
        await bot.delete_message(chat_id=message.from_user.id, message_id=(message.message_id - 1))
    except:
        pass

    user_data = await state.get_data()
    try:
        user_id = int(user_data['user_id'])
        user_upbalance = int(message.text)
    except:
        await message.answer('⚠️ Был указан неверный тип дынных')
        await state.clear()
        return

    try:
        Userx.user_change_balance(user_id=user_id, count=user_upbalance)
        await message.answer(f"✅ Пользователю: {user_id} добавлено {user_upbalance} berrycoins")
        await bot.send_message(chat_id=user_id, text=f'✅ Админ начислил Вам на баланс {user_upbalance} berrycoins!')
    except:
        await message.answer('⚠️ Произошла ошибка, вероятно в введённых данных')
        await state.clear()
        return

    await state.clear()


##### [ USER_BAN/UNBAN ] #####
# Изменения статуса бана пользователя
@router.callback_query(F.data == 'admin_ban_unban_user')
async def user_ban(call: CallbackQuery, bot: Bot, state: FSMContext):
    await call.message.delete()

    user_data = await state.get_data()

    try:
        user_id = int(user_data['user_id'])
        user_to_ban = user_id
        answer = Userx.user_ban_unban(user_to_ban)
        if answer:
            await call.message.answer(f'⛔ Пользователь {user_to_ban} был <b>забанен</b>')
            try:
                await bot.send_message(chat_id=user_to_ban, text='⛔ Вы были забанены администратором!\n'
                                                                 'Теперь Вы не сможете отправлять видео\n\n'
                                                                 '<b>Причина:</b> Без объяснения.')
            except:
                pass
        else:
            await call.message.answer(f'✅ Пользователь {user_to_ban} был <b>разбанен</b>')
            try:
                await bot.send_message(chat_id=user_to_ban, text='✅ Вы были разбанены администратором!\n'
                                                                 'Теперь Вы можете отправлять видео')
            except:
                pass
    except:
        await call.message.answer('⚠️ Некорректный id пользователя!\n'
                                  'Попробуйте заново')

    await state.clear()


##### [ USER_TIME ] #####
# Указание времени на добавление
@router.callback_query(F.data == 'admin_change_time')
async def choose_user(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите время, которое хотите добавить:')

    await state.set_state(AdminUser.user_change_time)


# Проверка и добавление времени
@router.message(AdminUser.user_change_time)
async def choose_user(message: Message, state: FSMContext):
    user_data = await state.get_data()
    try:
        user_id = int(user_data['user_id'])
        user_uptime = int(message.text)
    except:
        await message.answer('⚠️ Был указан неверный тип дынных')
        await state.clear()
        return

    try:
        Userx.user_uptime(user_id=user_id, minutes=user_uptime)
        await message.answer(f"✅ Время добавлено пользователю: {user_data['user_id']}, кол-во минут - {user_uptime}")
    except:
        await message.answer('⚠️ Произошла ошибка, вероятно в введённых данных')
        await state.clear()
        return

    await state.clear()
