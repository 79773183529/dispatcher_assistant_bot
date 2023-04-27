import datetime

import emoji
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot import bot
from inlineKeyboards import dynamic_time, dynamic_volume, dynamic_keyboard
from keyboardsCollection import *
from models import Client
from with_handler import del_old_message
from with_db import set_instance_by_class_and_id, set_application_list_by_creator, set_the_Application_by_id
from message_text import ButtonRedact, MessageRedact, MessageApplication, ButtonApplication
from settings import active_dispatcher_id_list
from with_handler import send_group_notification


class Redact(StatesGroup):
    waiting_for_application = State()
    waiting_for_action = State()
    waiting_for_time = State()
    waiting_for_volume = State()
    waiting_for_interval = State()


# Старт редактирования. Запрашивает выбор заявки из доступных к редактированию
async def start_redact(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    print(f"{user_id}  in  async def start_redact")
    try:
        client = set_instance_by_class_and_id(Client, user_id)
        applications_id_list = set_application_list_by_creator(client)
        await bot.send_message(user_id, emoji.emojize(":woman_technologist:"))
        await bot.send_message(user_id, f'Здравствуйте, {client.name}')
        if not applications_id_list:
            await bot.send_message(user_id, MessageRedact.start_error_no_application)
        else:
            await state.update_data(client=client)
            await state.update_data(applications_id_list=applications_id_list)
            msg = await bot.send_message(user_id, MessageRedact.start,
                                         reply_markup=make_keyboard_by_list(applications_id_list))
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(Redact.waiting_for_application.state)
    except (ValueError, IndexError):
        await bot.send_message(user_id, MessageRedact.start_error_not_client)


# Принимает заявку -> Запрашивает действие
async def get_application(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await del_old_message(bot, user_id, state)
    text = message.text
    user_data = await state.get_data()
    applications_id_list = user_data["applications_id_list"]
    if text not in map(str, applications_id_list):
        await bot.send_message(user_id, MessageRedact.request_appication_error)
        await state.finish()
    else:
        application = set_the_Application_by_id(the_id=int(text))
        await state.update_data(application=application)
        msg = await bot.send_message(user_id, MessageRedact.request_action,
                                     reply_markup=make_keyboard_by_list(ButtonRedact.actions_list))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Redact.waiting_for_action.state)


# Принимает название активности -> Запрашивает данные в зависимости от выбора активности
async def get_action(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await del_old_message(bot, user_id, state)
    text = message.text
    user_data = await state.get_data()
    application = user_data['application']
    client = application.creator
    product = application.product
    manager = application.manager
    the_object = application.the_object
    if text not in ButtonRedact.actions_list:
        await bot.send_message(user_id, MessageRedact.request_action_error)
        await state.finish()
    elif text == ButtonRedact.actions_list[0]:
        application.is_executed = True
        application.save()
        await bot.send_message(user_id, f"Хорошо {client.name}, подтверждение принято. Ожидайте пожалуйста "
                                        f"{product.product_type} в назначенное время.")

        await send_group_notification(bot=bot,
                                      list_id=[*active_dispatcher_id_list, manager.user_id],
                                      text=f"Внимание, клиент подтвердил готовность по заявке №{application.id}\n"
                                           f"принять {product.product_type} в количестве "
                                           f"{application.volume_declared} м3 "
                                           f"в {application.execution_time.strftime('%H:%M')}\n"
                                           f"на объект '{the_object.obj_name}':",
                                      location=the_object.location)
        await state.finish()
    elif text == ButtonRedact.actions_list[1]:
        time = application.execution_time
        msg = await bot.send_message(client.user_id, f"Изменить готовность на "
                                                     f"{time.strftime('%H часов %M минут')}",
                                     reply_markup=dynamic_time(time))
        await state.update_data(msg_id=msg.message_id)
        await state.update_data(time=time)
        await state.set_state(Redact.waiting_for_time.state)
    elif text == ButtonRedact.actions_list[2]:
        volume = application.volume_declared
        msg = await bot.send_message(user_id, f"Изменить количество {product.product_type} "
                                              f"на {volume} м3",
                                     reply_markup=dynamic_volume(volume))
        await state.update_data(msg_id=msg.message_id)
        await state.update_data(volume=volume)
        await state.set_state(Redact.waiting_for_volume.state)
    else:
        speed = application.declared_unloading_speed
        await bot.send_message(user_id, f"ОК Давайте изменим интервал отправки машин."
                                        f"Изначально мы определяли его из расчёта  "
                                        f"{speed} кубов в час")
        msg = await bot.send_message(user_id, f"Расчитать интервал из расчёта "
                                              f"{speed} кубов в час",
                                     reply_markup=dynamic_keyboard(speed))
        await state.update_data(msg_id=msg.message_id)
        await state.update_data(speed=speed)
        await state.set_state(Redact.waiting_for_interval.state)


# Принимает  время подачи. ->   КОЛЛБЕКИ
# Сохраняем изменения и информируем диспетчера и менеджера
async def get_time(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await del_old_message(bot, user_id, state)
    user_data = await state.get_data()
    application = user_data['application']
    time = user_data['time']
    product = application.product
    client = application.creator
    the_object = application.the_object
    now = datetime.datetime.now()
    if callback_query.data == 'now' and time > now:
        manager = application.manager
        application.execution_time = time
        application.save()
        await bot.send_message(user_id, f"Хорошо {client.name}, изменения принято. Не забудте не позднее чем за 2 часа"
                                        f" до этого времени подтвердить готовность на строительной площадки")
        await send_group_notification(bot=bot,
                                      list_id=[*active_dispatcher_id_list, manager.user_id],
                                      text=f"Клиент {client.name} {client.last_name} изменил время подачи "
                                           f"{product.product_type} по заявки №{application.id}  на  "
                                           f"{time.strftime('%H:%M')} на объект '{the_object.obj_name}':",
                                      location=the_object.location,
                                      src_photo=client.photo)
        await state.finish()
    else:
        if callback_query.data == 'now':
            await bot.send_message(user_id, f"К сожалению мы не сможем доставить вам {product.product_type} в "
                                            f"прошлое. Попробуйте выбрать другое время")
            sign = 0
        elif callback_query.data == 'forward':
            sign = 1
        else:
            sign = -1
        time += sign * datetime.timedelta(minutes=30)
        await state.update_data(time=time)
        msg = await bot.send_message(user_id, f"Изменить готовность на "
                                              f"{time.strftime('%H часов %M минут')}",
                                     reply_markup=dynamic_time(time))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Redact.waiting_for_time.state)


# Вспомогательная функция: Сохраняет изменения в БД и оповещает диспетчеров
async def save_and_send_to_dispatcher(state):
    user_data = await state.get_data()
    application = user_data['application']
    volume = user_data['volume']
    client = application.creator
    the_object = application.the_object
    manager = application.manager
    product = application.product
    volume_old = application.volume_declared
    application.volume_declared = volume
    application.save()
    time = application.execution_time
    time_before = time - datetime.timedelta(hours=2)
    await bot.send_message(client.user_id, f"Хорошо {client.name}, изменения принято. Не забудте не позднее чем до "
                                           f"{time_before.strftime('%H:%M')} подтвердить готовность на строительной"
                                           f" площадки или изменить время подачи")
    await send_group_notification(bot=bot,
                                  list_id=[*active_dispatcher_id_list, manager.user_id],
                                  text=f"Клиент {client.name} {client.last_name} изменил количество "
                                       f"{product.product_type}a по заявки №{application.id}  c  "
                                       f"{volume_old}м3  до {volume}м3 на объекте '{the_object.obj_name}':",
                                  location=the_object.location,
                                  src_photo=client.photo)


# Принимает  объём. ->   КОЛЛБЕКИ
# Сохраняет изиенения в БД и оповещает об изменениях диспетчеру
async def get_volume(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    await del_old_message(bot, user_id, state)
    user_data = await state.get_data()
    application = user_data['application']
    volume = user_data['volume']
    product = application.product
    if callback_query.data == 'send':
        await save_and_send_to_dispatcher(state)
        await state.finish()
    else:
        if callback_query.data == 'up':
            sign = 1
        else:
            sign = -1
        volume += sign * 0.5
        await state.update_data(volume=volume)
        msg = await bot.send_message(user_id, f"Подтвердити готовность принять {product.product_type} в "
                                              f"количестве {volume} м3",
                                     reply_markup=dynamic_volume(volume))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Redact.waiting_for_volume.state)


# Принимает  объём. ->   MESSAGE
# Сохраняет изменения в БД и оповещает об изменениях диспетчеру
async def get_volume2(message: types.Message, state: FSMContext):
    await del_old_message(bot, message, state)
    user_id = message.from_user.id
    volume = message.text
    try:
        volume = volume.replace(",", ".")
        await state.update_data(volume=float(volume))
        await save_and_send_to_dispatcher(state)
        await state.finish()
    except ValueError:
        msg = await bot.send_message(user_id, MessageApplication.request_volume_error)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Redact.waiting_for_volume.state)


# Вспомогательная функция: Сохраняет изменения в БД и оповещает диспетчеров
async def record_and_send_to_dispatcher(state):
    user_data = await state.get_data()
    application = user_data['application']
    speed = user_data['speed']
    client = application.creator
    the_object = application.the_object
    manager = application.manager
    product = application.product
    speed_old = application.declared_unloading_speed
    application.declared_unloading_speed = speed
    application.save()
    time = application.execution_time
    time_before = time - datetime.timedelta(hours=2)
    await bot.send_message(client.user_id, f"Хорошо {client.name}, изменения принято. Не забудте не позднее чем до "
                                           f"{time_before.strftime('%H:%M')} подтвердить готовность на строительной"
                                           f" площадки или изменить время подачи")
    await send_group_notification(bot=bot,
                                  list_id=[*active_dispatcher_id_list, manager.user_id],
                                  text=f"Клиент {client.name} {client.last_name} изменил скорость разгрузки "
                                       f"{product.product_type}a по заявки №{application.id}  c  "
                                       f"{speed_old}м3/час  до {speed}м3/час на объекте '{the_object.obj_name}':",
                                  location=the_object.location,
                                  src_photo=client.photo)


# Принимает  скорость разгрузки. ->   КОЛЛБЕКИ
# (Запрашивает длину стрелы бетононасоса)    или   (Записывает Application в БД -> Отправляет заявку менеджеру)
async def get_speed(callback_query: types.CallbackQuery, state: FSMContext):
    print("async def new_test(callback_query: types.CallbackQuery, state: FSMContext)")
    user_id = callback_query.from_user.id
    await del_old_message(bot, user_id, state)
    user_data = await state.get_data()
    application = user_data['application']
    if application.unloading_method == ButtonApplication.unloading_method_list[1]:
        step = 5
    else:
        step = 0.5
    speed = user_data['speed']
    if callback_query.data == 'send':
        await state.update_data(declared_unloading_speed=speed)
        await record_and_send_to_dispatcher(state)
    else:
        if callback_query.data == 'up':
            sign = 1
        else:
            sign = -1
        speed += sign * step
        await state.update_data(speed=speed)
        msg = await bot.send_message(user_id, f"Расчитать интервал из расчёта "
                                              f"{speed} кубов в час",
                                     reply_markup=dynamic_keyboard(speed))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Redact.waiting_for_interval.state)


def register_handlers_redact(dp: Dispatcher):
    dp.register_message_handler(start_redact, commands="redact", state="*")
    dp.register_message_handler(get_application, state=Redact.waiting_for_application)
    dp.register_message_handler(get_action, state=Redact.waiting_for_action)
    dp.register_callback_query_handler(get_time, state=Redact.waiting_for_time)
    dp.register_callback_query_handler(get_volume, state=Redact.waiting_for_volume)
    dp.register_message_handler(get_volume2, state=Redact.waiting_for_volume)
    dp.register_callback_query_handler(get_speed, state=Redact.waiting_for_interval)
