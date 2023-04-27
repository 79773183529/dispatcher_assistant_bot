import emoji
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot import bot
from keyboardsCollection import *
from models import Driver
from with_db import set_instance_by_class_and_id


class DriverOn(StatesGroup):
    waiting_for_answer = State()


# Старт сессии. Запрашивает статус  is_work
async def start_work(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    print(f"{user_id}  in  async def start_driver_on")
    try:
        driver = set_instance_by_class_and_id(Driver, user_id)
        await bot.send_message(user_id, emoji.emojize(":woman_technologist:"))
        await bot.send_message(user_id, f'Здравствуйте, {driver.name}')
        await state.update_data(driver=driver)
        await bot.send_message(user_id, "Нажмите 'ON' чтобы начать работать или 'OFF' чтобы закончить",
                               reply_markup=make_keyboard_by_list_only(["ON", "OFF"]))
        await state.set_state(DriverOn.waiting_for_answer.state)
    except (ValueError, IndexError):
        await bot.send_message(user_id, "Опция доступна только для пользователей зарегестрированных "
                                        "в приложении как водитель")


# Принимает ответ -> Записывает изменения в БД
async def get_answer(message: types.Message, state: FSMContext):
    text = message.text
    user_data = await state.get_data()
    driver = user_data['driver']
    if text == "ON":
        driver.is_work = True
        driver.save()
        await message.answer("Вы подключились. Желаю плодотворной работы", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    elif text == "OFF":
        driver.is_work = False
        driver.save()
        await message.answer("Вы отключились. Желаю хорошего отдыха", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer("Пожалуйста нажмите на кнопку")


def register_handlers_driver_on(dp: Dispatcher):
    dp.register_message_handler(start_work, commands="on", state="*")
    dp.register_message_handler(get_answer, state=DriverOn.waiting_for_answer)
