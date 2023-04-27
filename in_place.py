from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import datetime

from bot import bot
from keyboardsCollection import *
from models import Driver
from with_db import set_instance_by_class_and_id
from message_text import MessageSendLocation, MessageInPlace, MessageApplication, ButtonApplication
from inlineKeyboards import dynamic_score


class InPlace(StatesGroup):
    waiting_for_free = State()
    waiting_for_score = State()


# Старт запроса локации. Запрашивает выбор водителя
async def start_in_place(message: types.Message, state: FSMContext):
    print(f"{message.from_user.id}  in  async def start_in_place")
    try:
        driver = set_instance_by_class_and_id(Driver, message.from_user.id)
        application = driver.working_by_application
        if not application:
            await message.answer(MessageInPlace.not_application, reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
        else:
            start = datetime.datetime.now()
            await state.update_data(driver=driver)
            await state.update_data(start=start)
            await state.update_data(application=application)
            await message.answer(MessageInPlace.start, reply_markup=make_keyboard_by_list_only(['Освободился']))
            await state.set_state(InPlace.waiting_for_free.state)
    except (ValueError, IndexError):
        await message.answer(MessageSendLocation.push_location_error)
        await state.finish()


# Принимает событие что водитель освободился. Запрашивает оценку объекта
async def get_free(message: types.Message, state: FSMContext):
    if message.text == "Освободился":
        user_data = await state.get_data()
        application = user_data["application"]
        start = user_data["start"]
        driver = user_data["driver"]
        delta = datetime.datetime.now() - start
        the_object = application.the_object
        mixer = driver.mixer
        volume = mixer.max_volume
        delta = delta.seconds/3600
        delta = volume/delta
        await state.update_data(the_object=the_object)
        if application.unloading_method == ButtonApplication.unloading_method_list[0]:
            if the_object.average_speed_of_unloading_by_crane:
                the_object.average_speed_of_unloading_by_crane = \
                    (the_object.average_speed_of_unloading_by_crane + delta) / 2
            else:
                the_object.average_speed_of_unloading_by_crane = delta
        elif application.unloading_method == ButtonApplication.unloading_method_list[1]:
            if the_object.average_speed_of_unloading_by_pump:
                the_object.average_speed_of_unloading_by_pump = \
                    (the_object.average_speed_of_unloading_by_pump + delta) / 2
            else:
                the_object.average_speed_of_unloading_by_pump = delta
        else:
            if the_object.average_speed_of_unloading_by_self_watering:
                the_object.average_speed_of_unloading_by_self_watering = \
                    (the_object.average_speed_of_unloading_by_self_watering + delta) / 2
            else:
                the_object.average_speed_of_unloading_by_self_watering = delta
        the_object.save()
        score = 7
        await message.answer("Принято", reply_markup=types.ReplyKeyboardRemove())
        msg = await message.answer(MessageInPlace.request_score, reply_markup=dynamic_score(score))
        await state.update_data(msg=msg, score=score)
        await state.set_state(InPlace.waiting_for_score.state)


# Принимает  оценку объекта. ->   КОЛЛБЕКИ
# Сохраняет изиенения в БД и оповещает  диспетчера
async def get_score(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    user_data = await state.get_data()
    score = user_data['score']
    msg = user_data['msg']
    the_object = user_data['the_object']
    driver = user_data['driver']
    if callback_query.data == 'send':
        await bot.send_message(user_id, MessageInPlace.thanks, reply_markup=types.ReplyKeyboardRemove())
        if the_object.condition_of_access_roads:
            the_object.condition_of_access_roads = (the_object.condition_of_access_roads + score)/2
        else:
            the_object.condition_of_access_roads = score
        the_object.save()
        driver.working_by_application = None
        driver.save()
        await callback_query.answer()
        await state.finish()
    else:
        if callback_query.data == 'up':
            print("up")
            sign = 1
        else:
            print("down")
            sign = -1
        score += sign
        if 0 <= score <= 10:
            await state.update_data(score=score)
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=msg.message_id,
                                                reply_markup=dynamic_score(score))
        await callback_query.answer()




def register_handlers_send_in_place(dp: Dispatcher):
    dp.register_message_handler(start_in_place, commands="object", state="*")
    dp.register_message_handler(get_free, state=InPlace.waiting_for_free)
    dp.register_callback_query_handler(get_score, state=InPlace.waiting_for_score)
