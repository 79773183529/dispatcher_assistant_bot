import asyncio
from typing import Any

import emoji
from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


# Удаляет предидущее сообщение 2
async def del_old_message(bot: Bot, user_id, state: FSMContext):
    user_data = await state.get_data()
    try:
        msg_id = user_data["msg_id"]
        await bot.delete_message(chat_id=user_id, message_id=msg_id)
    except Exception as err:
        print(err)


# Вспомогательная функция принимает локацию из БД и user_id -> отправляет смс с геолокацией на карте
async def pars_and_send_location(bot: Bot, location, user_id):
    try:
        latitude = location.latitude
        longitude = location.longitude
        print('location = ', location)
        print('location = ', type(location))
    except AttributeError:
        print('location = ', location)
        print('location = ', type(location))
        latitude = float(location.split(',')[0].strip(" {}").split(' ')[1])
        longitude = float(location.split(',')[1].strip(" {}").split(' ')[1])
    await bot.send_location(user_id, latitude, longitude)


# Принимае список id + текст сообщения -> отпровляет сообщение всем кто в списке
async def send_group_messages(bot: Bot, list_id: list, text: str):
    for user_id in list_id:
        await bot.send_message(user_id, text)
        await asyncio.sleep(1)


# Принимает список id + текст сообщения + локацию -> отпровляет сообщение и локацию всем кто в списке
async def send_group_notification(bot: Bot, list_id: list, text: str, location: Any, src_photo=None):
    for user_id in list_id:
        if src_photo:
            with open(src_photo, 'rb') as photo:
                await bot.send_photo(user_id, photo)
        else:
            await bot.send_message(user_id, emoji.emojize(":woman_raising_hand:"))
        await bot.send_message(user_id, text)
        await pars_and_send_location(bot, user_id=user_id, location=location)
        await asyncio.sleep(1)
