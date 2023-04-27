import asyncio
import datetime

import emoji
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot import bot
from inlineKeyboards import dynamic_time, dynamic_volume, dynamic_keyboard
from keyboardsCollection import *
from models import Dispatcher, Driver
from with_handler import del_old_message, pars_and_send_location
from with_db import *
from message_text import MessageWork, work_message_to_disp_for_approve, approve_answer_to_disp, \
    work_message_to_client_for_departure_mixer, work_message_to_driver
from settings import active_dispatcher_id_list
from with_handler import send_group_notification


class Work(StatesGroup):
    waiting_for_application = State()
    waiting_for_driver = State()
    waiting_for_volume = State()
    waiting_for_time = State()
    waiting_for_approve = State()


# Старт рабочей сессии. Запрашивает номер заявки из доступных
async def start_work(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    print(f"{user_id}  in  async def start_work")
    try:
        dispatcher = set_instance_by_class_and_id(Dispatcher, user_id)
        applications_id_list = set_executed_application_list()
        await bot.send_message(user_id, emoji.emojize(":woman_technologist:"))
        await bot.send_message(user_id, f'Здравствуйте, {dispatcher.name}')
        if not applications_id_list:
            await bot.send_message(user_id, MessageWork.start_error_no_application)
        else:
            await state.update_data(dispatcher=dispatcher)
            await state.update_data(applications_id_list=applications_id_list)
            msg = await bot.send_message(user_id, MessageWork.request_application,
                                         reply_markup=make_keyboard_by_list(applications_id_list))
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(Work.waiting_for_application.state)
    except (ValueError, IndexError):
        await bot.send_message(user_id, MessageWork.start_error_not_client)


# Принимает заявку -> Запрашивает водителя
async def get_application(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await del_old_message(bot, user_id, state)
    text = message.text
    user_data = await state.get_data()
    applications_id_list = user_data["applications_id_list"]
    if text not in map(str, applications_id_list):
        await bot.send_message(user_id, MessageWork.request_application_error)
        await state.finish()
    else:
        application = set_the_Application_by_id(the_id=int(text))
        await state.update_data(application=application)
        driver_list = set_free_driver_list()
        msg = await bot.send_message(user_id, MessageWork.request_driver,
                                     reply_markup=make_keyboard_by_list(driver_list))
        await state.update_data(driver_list=driver_list)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Work.waiting_for_driver.state)


# Принимает водителя -> Запрашивает объём
async def get_driver(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await del_old_message(bot, user_id, state)
    try:
        driver_id = int(message.text.split()[0].strip("№"))  # вычлиняем из надписи на кнопки  id водителя
        driver = set_instance_by_class_and_id1(Driver, driver_id)
        await state.update_data(driver=driver)
        mixer = driver.mixer
        volume = mixer.max_volume
        await state.update_data(volume=volume)
        msg = await bot.send_message(user_id, MessageWork.request_volume,
                                     reply_markup=dynamic_volume(volume))
        await state.update_data(msg=msg)
        await state.set_state(Work.waiting_for_volume.state)
    except Exception as err:
        print('error: ', err)
        user_data = await state.get_data()
        driver_list = user_data['driver_list']
        msg = await bot.send_message(user_id, MessageWork.request_driver_error,
                                     reply_markup=make_keyboard_by_list(driver_list))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Work.waiting_for_driver.state)


# Принимает  объём. ->   КОЛЛБЕКИ
# Запрашивает ориентировочное время прибытия
async def get_volume(callback_query: types.CallbackQuery, state: FSMContext):
    print("def get_volume in work")
    user_id = callback_query.from_user.id
    user_data = await state.get_data()
    volume = user_data['volume']
    if callback_query.data == 'send':
        await callback_query.answer()
        await bot.send_message(user_id, MessageWork.request_travel_time)
        await state.set_state(Work.waiting_for_time.state)
    else:
        if callback_query.data == 'up':
            print("up")
            sign = 1
        else:
            print("down")
            sign = -1
        volume += sign * 0.5
        msg = user_data['msg']
        await state.update_data(volume=volume)
        await msg.edit_reply_markup(dynamic_volume(volume))
        await state.set_state(Work.waiting_for_volume.state)


# Принимает  объём. ->   MESSAGE
# Запрашивает ориентировочное время прибытия
async def get_volume2(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    volume = message.text
    try:
        volume = volume.replace(",", ".")
        await state.update_data(volume=float(volume))
        await bot.send_message(user_id, MessageWork.request_travel_time)
        await state.set_state(Work.waiting_for_time.state)
    except ValueError:
        await bot.send_message(user_id, MessageWork.request_volume_error)
        await state.set_state(Work.waiting_for_volume.state)


# Принимает  ориентировочное время прибытия  -> Запрашивает подтверждение
async def get_time(message: types.Message, state: FSMContext):
    text = message.text
    try:
        the_time = datetime.datetime.strptime(text, "%H:%M")
        print('the_time = ', the_time)
        await state.update_data(time=the_time)
        await message.answer(emoji.emojize(":woman_technologist:"))
        text = await work_message_to_disp_for_approve(state)
        await message.answer(text,
                             reply_markup=make_keyboard_by_list_only(["Да правильно", "Нет нужно переделать"]))
        await state.set_state(Work.waiting_for_approve.state)
    except ValueError:
        await message.answer(MessageWork.request_travel_time_error)
        await state.set_state(Work.waiting_for_time.state)


# Принимает подтверждение  ->
async def get_approve(message: types.Message, state: FSMContext):
    text = message.text
    if text == "Да правильно":
        user_data = await state.get_data()
        driver = user_data['driver']
        application = user_data['application']
        volume = user_data['volume']
        client = application.creator
        if application.volume_total:
            application.volume_total += volume
        else:
            application.volume_total = volume
        application.save()
        await asyncio.sleep(2)
        remainder = application.volume_declared - application.volume_total
        application.volume_remains = remainder
        application.save()
        driver.working_by_application = application
        driver.save()
        the_object = application.the_object
        if the_object.total_number:
            the_object.total_number += volume
        else:
            the_object.total_number = volume
        the_object.save()
        await state.update_data(remainder=remainder)

        await message.answer(approve_answer_to_disp(remainder), reply_markup=types.ReplyKeyboardRemove())
        await asyncio.sleep(2)

        text = await work_message_to_client_for_departure_mixer(state)
        await bot.send_message(client.user_id, text)
        await asyncio.sleep(2)

        text = await work_message_to_driver(state)
        await bot.send_message(driver.user_id, text)
        await pars_and_send_location(bot=bot, user_id=driver.user_id, location=the_object.location)
        await bot.send_message(driver.user_id, MessageWork.end, reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer(MessageWork.approve_error, reply_markup=types.ReplyKeyboardRemove())
        await state.finish()


def register_handlers_work(dp: Dispatcher):
    dp.register_message_handler(start_work, commands="work", state="*")
    dp.register_message_handler(get_application, state=Work.waiting_for_application)
    dp.register_message_handler(get_driver, state=Work.waiting_for_driver)
    dp.register_callback_query_handler(get_volume, state=Work.waiting_for_volume)
    dp.register_message_handler(get_volume2, state=Work.waiting_for_volume)
    dp.register_message_handler(get_time, state=Work.waiting_for_time)
    dp.register_message_handler(get_approve, state=Work.waiting_for_approve)
