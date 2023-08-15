from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

item_1 = KeyboardButton('Все')
item_2 = KeyboardButton('Без исполнителя')
item_3 = KeyboardButton('Уведомления')

main_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder="Выберите команду")

main_menu.row(item_1, item_2)
main_menu.row(item_3)


off = KeyboardButton('❌Выключить')
back = KeyboardButton('🔙Назад')

notice_off = ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder="Выберите команду")

notice_off.row(off)
notice_off.row(back)


on = KeyboardButton('✅Включить')
back = KeyboardButton('🔙Назад')

notice_on = ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder="Выберите команду")

notice_on.row(on)
notice_on.row(back)