from app import keyboards as kb
from app.parser import convert_data
from main import dp
from app import database as db
from aiogram.types import Message
from aiogram import types


@dp.message_handler(commands=['start', 'user'])
async def start(message: Message):
    await db.user_exists(message.from_user.id)
    await message.answer('👋Добро пожаловать!', reply_markup=kb.main_menu)


@dp.message_handler(lambda message: message.text in ['✅Включить', '❌Выключить'])
async def switcher_handler(message: types.Message):
    if message.text == '✅Включить':
        await db.switch_notice(message.from_user.id, 'on')
        await message.answer('Изменение применено🎉', reply_markup=kb.notice_off)

    elif message.text == '❌Выключить':
        await db.switch_notice(message.from_user.id, 'off')
        await message.answer('Изменение применено🎉', reply_markup=kb.notice_on)


@dp.message_handler(content_types=['text'])
async def user_buttons(message: Message):

    if message.text == 'Все':
        file_path = convert_data('all')
        with open(file_path, 'rb') as file:
            await message.reply_document(file)

    elif message.text == 'Без исполнителя':
        file_path = convert_data('unexecuted')
        with open(file_path, 'rb') as file:
            await message.reply_document(file)

    elif message.text == 'Уведомления':

        if await db.check_notice(message.from_user.id) == 1:
            await message.answer('Здесь вы можете включить или выключить уведомления. '
                                 '\n\nНа данный момент уведомления - ➡Включены', reply_markup=kb.notice_off)

        else:
            await message.answer('Здесь вы можете включить или выключить уведомления. '
                                 '\n\nНа данный момент уведомления - ➡Выключены', reply_markup=kb.notice_on)

    elif message.text == '🔙Назад':
        await message.answer('Возвращаю в главное меню!', reply_markup=kb.main_menu)

    else:
        await message.answer('Команда не распознана, возвращаю в главное меню!', reply_markup=kb.main_menu)
