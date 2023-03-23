import os
import logging
import requests

from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv

from keyboards import keyboard_start, keyboard_num_system, keyboard_info


load_dotenv()

TOKEN = os.getenv('TOKEN')
CHAT_TOKEN = os.getenv('CHAT_ID')
OPEN_WEATHER_TOKEN = os.getenv('OPEN_WEATHER_TOKEN')
LIST_COMMAND = '''
<b>/start</b> - <em>запускает infoIT2107 бота</em>\n
<b>/help</b> - <em>список команд бота</em>\n
'''
LIST_OF_CALLS = '''
<b>1 урок</b> - 08:30-09:15 \n
<b>2 урок</b> - 09:25-10:10 \n
<b>3 урок</b> - 10:30-11:15 \n
<b>4 урок</b> - 11:30-12:15 \n
<b>5 урок</b> - 12:25-13:10 \n
<b>6 урок</b> - 13:30-14:15 \n
<b>7 урок</b> - 14:30-15:15 \n
<b>8 урок</b> - 15:25-16:10 \n
'''


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    number = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(
        text='Здравствуйте! Помогу чем смогу...\n' + LIST_COMMAND,
        reply_markup=keyboard_start,
        parse_mode='HTML',
    )


@dp.message_handler(lambda message: message.text == '🔙 Назад')
async def back_command(message: types.Message):
    await message.answer(
        text='Основное меню',
        reply_markup=keyboard_start,
    )
    await message.delete()


@dp.message_handler(lambda message: message.text == 'Информация')
async def info_command(message: types.Message):
    await message.answer(
        text='Информация',
        reply_markup=keyboard_info,
    )
    await message.delete()


@dp.message_handler(lambda message: message.text == 'Расписание звонков')
async def list_of_call(message: types.Message):
    await message.answer(
        text='🔔РАСПИСАНИЕ ЗВОНКОВ🔔\n' + LIST_OF_CALLS,
        parse_mode='HTML',
    )
    await message.delete()


@dp.message_handler(lambda message: message.text == 'Системы счисления')
async def num_system(message: types.Message):
    await message.answer(
        text='В этом разделе можно перевести число в указаные системы счисления.\n'
             'Выберите основание 🔢',
        reply_markup=keyboard_num_system,
    )
    await message.delete()


@dp.message_handler(lambda message:
                    message.text == 'Двоичная' or
                    message.text == 'Восьмиричная' or
                    message.text == 'Шестнадцатиричная' or
                    message.text == 'Десятичная'
                    )
async def num_system(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['num_system'] = message.text
    if message.text == 'Десятичная':
        await message.answer(text='Введите число и через пробел укажите основание системы счисления.')
    else:
        await message.answer(text='Введите десятичное число с клавиатуры.')
    await Form.number.set()


@dp.message_handler(state=Form.number)
async def num_system_code(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        try:
            number = message.text
            if proxy['num_system'] == 'Двоичная':
                number = bin(int(number))[2:]
            elif proxy['num_system'] == 'Восьмиричная':
                number = oct(int(number))[2:]
            elif proxy['num_system'] == 'Шестнадцатиричная':
                number = hex(int(number))[2:]
                number = number.upper()
            elif proxy['num_system'] == 'Десятичная':
                number, n_system = number.split()
                number = int(number.lower(), int(n_system))
            await message.answer(number)
            await state.finish()
        except ValueError:
            await message.delete()
            await message.answer(
                text='Неккоректный ввод числа. Выберите систему счисления снова.',
                reply_markup=keyboard_num_system,
            )
            await state.finish()


@dp.message_handler(lambda message: message.text == 'Конец учебного года')
async def end_year(message: types.Message):
    end_time = datetime(2023, 5, 25)
    time_now = datetime.now()
    time_delta = end_time - time_now
    time_delta = time_delta.days
    await message.delete()
    await message.answer(f'До конца учебного года осталось {time_delta} д.')


@dp.message_handler(lambda message: message.text == 'Получить котика 🐈')
async def end_year(message: types.Message):
    response = requests.get(url='https://api.thecatapi.com/v1/images/search').json()
    random_cat = response[0].get('url')
    await message.delete()
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_cat,
    )


@dp.message_handler(lambda message: message.text == 'Температура на улице')
async def get_weather(message: types.Message):
    address = 'https://ipinfo.io/json'
    response = requests.get(url=address).json()
    lat, lon = response['loc'].split(',')
    params = {
        'lat': lat,
        'lon': lon,
        'appid': '87da88c8017d9374989a48ebba1e3e52',
        'units': 'metric',
    }
    address = 'https://api.openweathermap.org/data/2.5/weather?'
    response = requests.get(url=address, params=params).json()
    response = response.get('main')
    temp = round(response['temp'])
    await message.delete()
    await message.answer(text=f'Температура на улице {temp} ℃')


@dp.message_handler(lambda message: message.text == 'Показать мой IP')
async def get_ip_address(message: types.Message):
    address = 'https://ipinfo.io/json'
    response = requests.get(url=address).json()
    ip_address = response['ip']
    await message.delete()
    await message.answer(text=f'Ваш ip-адрес - {ip_address}')


if __name__ == '__main__':
    executor.start_polling(
        dp,
        skip_updates=True,  # Игнорировать все сообщения в оффлайн режиме
    )
