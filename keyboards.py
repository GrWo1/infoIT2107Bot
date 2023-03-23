from aiogram.types import (
                        KeyboardButton,
                        ReplyKeyboardMarkup,
                        InlineKeyboardMarkup,
                        InlineKeyboardButton,
                    )


keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_info = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_num_system = ReplyKeyboardMarkup(resize_keyboard=True)
buttons_start = [
    'Информация',
    'Системы счисления',
    'Литература',
    'Видео',
]
buttons_back = ['🔙 Назад']
buttons_cat = 'Получить котика 🐈'
buttons_info = [
    'Расписание звонков',
    'Температура на улице',
    'Конец учебного года',
    'Показать мой IP',
]
buttons_num_system = [
    'Десятичная',
    'Двоичная',
    'Восьмиричная',
    'Шестнадцатиричная',
]
keyboard_start.add(*buttons_start).add(buttons_cat)
keyboard_info.add(*buttons_info).add(*buttons_back)
keyboard_num_system.add(*buttons_num_system).add(*buttons_back)
