import datetime

import emoji
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot import bot
from keyboardsCollection import *
from models import Dispatcher, Manager
from with_handler import del_old_message
from with_db import set_instance_by_class_and_id, set_application_list_by_datetime
from message_text import MessageRedact, MessageApplication, ButtonApplication, MessageUploading
from with_file import fill_file


class Uploading(StatesGroup):
    waiting_for_date = State()


# Старт . Запрашивает дату на которую нужны данные
async def start_uploading(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    print(f"{user_id}  in  async def start_redact")
    try:
        try:
            the_user = set_instance_by_class_and_id(Dispatcher, user_id)
        except (ValueError, IndexError):
            the_user = set_instance_by_class_and_id(Manager, user_id)
        await bot.send_message(user_id, emoji.emojize(":woman_technologist:"))
        await bot.send_message(user_id, f'Здравствуйте, {the_user.name}')
        await state.update_data(the_user=the_user)
        msg = await bot.send_message(user_id, MessageUploading.request_date,
                                     reply_markup=make_keyboard_by_list(ButtonApplication.date_list,
                                                                        ButtonApplication.today))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Uploading.waiting_for_date.state)

    except (ValueError, IndexError):
        await bot.send_message(user_id, MessageRedact.start_error_not_client)


# Принимает  дату. -> Отправляет эксель файл с данными
async def get_date(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await del_old_message(bot, user_id, state)
    text = message.text
    try:
        if text == ButtonApplication.date_list[0]:
            the_date = datetime.datetime.today() + datetime.timedelta(days=1)
        elif text == ButtonApplication.date_list[1]:
            the_date = datetime.datetime.today() + datetime.timedelta(days=2)
        elif text == ButtonApplication.today:
            the_date = datetime.datetime.today()
        else:
            the_date = datetime.datetime.strptime(text, "%d.%m.%Y")
        the_date = the_date.replace(hour=0, minute=0, second=0, microsecond=0)
        print('the_date = ', the_date)
        applications_list = set_application_list_by_datetime(the_date)
        src = fill_file(applications_list)
        print("src = ", src)
        await bot.send_message(user_id, "Вот файл с выгрузкой заявок")
        doc = open(src, 'rb')
        await bot.send_document(user_id, doc)
    except ValueError:
        msg = await bot.send_message(user_id, MessageApplication.request_date_error)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Uploading.waiting_for_date.state)


def register_handlers_uploading(dp: Dispatcher):
    dp.register_message_handler(start_uploading, commands="uploading", state="*")
    dp.register_message_handler(get_date, state=Uploading.waiting_for_date)
