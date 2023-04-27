import emoji
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot import bot
from keyboardsCollection import *
from models import Client, Driver
from with_db import set_instance_by_class_and_id, set_executed_application_list_by_creator,\
    set_busy_driver_list_by_applications, set_instance_by_class_and_id1
from message_text import MessageRedact, MessageGetLocation, get_location_from_driver



class GetLocation(StatesGroup):
    waiting_for_driver = State()


# Старт запроса локации. Запрашивает выбор водителя
async def start_get_location(message: types.Message, state: FSMContext):
    print(f"{message.from_user.id}  in  async def start_redact")
    try:
        client = set_instance_by_class_and_id(Client, message.from_user.id)
        applications_list = set_executed_application_list_by_creator(client)
        if not applications_list:
            await message.answer(MessageGetLocation.no_application, reply_markup=types.ReplyKeyboardRemove())
        else:
            driver_list = set_busy_driver_list_by_applications(applications_list)
            await message.answer(emoji.emojize(":woman_technologist:"))
            if not driver_list:
                await message.answer(MessageGetLocation.no_drivers, reply_markup=types.ReplyKeyboardRemove())
            else:
                await state.update_data(client=client)
                await state.update_data(driver_list=driver_list)
                await message.answer(MessageGetLocation.request_driver,
                                     reply_markup=make_keyboard_by_list_only(driver_list))
                await state.set_state(GetLocation.waiting_for_driver.state)
    except (ValueError, IndexError):
        await message.answer(MessageRedact.start_error_not_client)



# Принимает водителя -> Запрашивает  у него геолокацию
async def get_driver(message: types.Message, state: FSMContext):
    try:
        driver_id = int(message.text.split()[0].strip("№"))  # вычлиняем из надписи на кнопки  id водителя
        driver = set_instance_by_class_and_id1(Driver, driver_id)
        await state.update_data(driver=driver)
        await message.answer(MessageGetLocation.notice, reply_markup=types.ReplyKeyboardRemove())
        text = await get_location_from_driver(state)
        await bot.send_message(driver.user_id, emoji.emojize(":woman_technologist:"))
        await bot.send_message(driver.user_id, text, reply_markup=types.ReplyKeyboardRemove())
    except Exception as err:
        print('error: ', err)
        await bot.send_message(message.from_user.id, MessageGetLocation.request_driver_error,
                               reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_get_location(dp: Dispatcher):
    dp.register_message_handler(start_get_location, commands="Get_location", state="*")
    dp.register_message_handler(get_driver, state=GetLocation.waiting_for_driver)
