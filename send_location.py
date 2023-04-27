from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot import bot
from keyboardsCollection import *
from models import Driver
from with_db import set_instance_by_class_and_id
from message_text import MessageSendLocation, set_location_from_driver, set_location_from_driver_error


class SendLocation(StatesGroup):
    waiting_for_answer = State()   


# Старт запроса локации. Запрашивает выбор водителя
async def start_send_location(message: types.Message, state: FSMContext):
    print(f"{message.from_user.id}  in  async def send_location")
    try:
        driver = set_instance_by_class_and_id(Driver, message.from_user.id)
        application = driver.working_by_application
        client = application.creator
        await state.update_data(driver=driver, client=client)
        await message.answer(MessageSendLocation.push_location, reply_markup=make_keyboard_location())
        await state.set_state(SendLocation.waiting_for_answer.state)
    except (ValueError, IndexError):
        await message.answer(MessageSendLocation.push_location_error)


# Принимает   и перенаправляет клиенту геолокацию
async def get_location(message: types.Message, state: FSMContext):
    print("Heloo !!!!!!!!!!! from get_location")
    location = message.location
    user_data = await state.get_data()
    client = user_data['client']
    text = await set_location_from_driver(state)
    await bot.send_message(client.user_id, text, reply_markup=types.ReplyKeyboardRemove())
    await bot.send_location(client.user_id, longitude=location.longitude, latitude=location.latitude)
    await state.finish()


# Принимает геолокацию2 (если геолокация не отправлена) запрашивает фото
async def get_location2(message: types.Message, state: FSMContext):
    print("Heloo !!!!!!!!!!! from get_location2222222222222")
    user_data = await state.get_data()
    client = user_data['client']
    text = await set_location_from_driver_error(state)
    await bot.send_message(client.user_id, text, reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_send_location(dp: Dispatcher):
    dp.register_message_handler(start_send_location, commands="Send_location", state="*")
    dp.register_message_handler(get_location,
                                state=SendLocation.waiting_for_answer,
                                content_types=types.ContentType.LOCATION)
    dp.register_message_handler(get_location2, state=SendLocation.waiting_for_answer)
