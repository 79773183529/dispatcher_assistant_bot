import emoji
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot import bot
from inlineKeyboards import dynamic_time, dynamic_volume, dynamic_keyboard
from keyboardsCollection import *
from models import Client
from with_handler import del_old_message
from with_db import set_instance_by_class_and_id, set_application_list_by_creator_for_del, set_the_Application_by_id
from message_text import ButtonRedact, MessageRedact, MessageDelete
from settings import active_dispatcher_id_list
from with_handler import send_group_notification


class Delete(StatesGroup):
    waiting_for_application = State()


# Старт процедуры удаления заявки. Запрашивает выбор заявки из доступных
async def start_delete(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    print(f"{user_id}  in  async def start_delete")
    try:
        client = set_instance_by_class_and_id(Client, user_id)
        applications_id_list = set_application_list_by_creator_for_del(client)
        await bot.send_message(user_id, emoji.emojize(":woman_technologist:"))
        await bot.send_message(user_id, f'Здравствуйте, {client.name}')
        if not applications_id_list:
            await bot.send_message(user_id, MessageDelete.start_error_no_application)
        else:
            await state.update_data(client=client)
            await state.update_data(applications_id_list=applications_id_list)
            msg = await bot.send_message(user_id, MessageDelete.start,
                                         reply_markup=make_keyboard_by_list(applications_id_list))
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(Delete.waiting_for_application.state)
    except (ValueError, IndexError):
        await bot.send_message(user_id, MessageRedact.start_error_not_client)


# Принимает номер заявки -> Удаляет её и оповещает всех
async def get_application(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await del_old_message(bot, user_id, state)
    text = message.text
    user_data = await state.get_data()
    applications_id_list = user_data["applications_id_list"]
    if text not in map(str, applications_id_list):
        await bot.send_message(user_id, MessageDelete.request_appication_error)
        await state.finish()
    else:
        application = set_the_Application_by_id(the_id=int(text))
        client = application.creator
        manager = client.person_manager
        product = application.product
        the_object = application.the_object
        application.is_delete = True
        application.is_active = False
        application.save()
        await bot.send_message(user_id, f"Хорошо {client.name}, заявка №{application.id} отменена ")

        await send_group_notification(bot=bot,
                                      list_id=[*active_dispatcher_id_list, manager.user_id],
                                      text=f"Внимание, клиент отменил заявку №{application.id}:\n"
                                           f"{product.product_type} в количестве "
                                           f"{application.volume_declared} м3 "
                                           f"в {application.execution_time.strftime('%H:%M')}\n"
                                           f"на объект '{the_object.obj_name}':",
                                      location=the_object.location)
        await state.finish()


def register_handlers_delete(dp: Dispatcher):
    dp.register_message_handler(start_delete, commands="delete", state="*")
    dp.register_message_handler(get_application, state=Delete.waiting_for_application)
