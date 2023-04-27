import asyncio
import datetime

import emoji
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types, Dispatcher

from registration import del_old_message, del_old_message2
from with_handler import pars_and_send_location
from with_db import set_application_by_time
from bot import bot, scheduler, dp
from keyboardsCollection import make_keyboard_by_list_only
from inlineKeyboards import dynamic_time, dynamic_volume
from settings import active_dispatcher_id_list
from message_text import MessageApplication


class Reminder(StatesGroup):
    waiting_for_approved = State()
    waiting_for_approved_time = State()
    waiting_for_approved_volume = State()


# Добавляем задачу в планировщик
def schedule_jobs():
    scheduler.add_job(send_message_in_time, "interval", seconds=30, minutes=30)


# Проверяет есть ли подходящие по времени заявки и отправляет их создателю требование подтвердить готовность
async def send_message_in_time():
    print("schedule job")
    application_list = set_application_by_time()
    if application_list:
        for application in application_list:
            client = application.creator
            product = application.product
            the_object = application.the_object
            await bot.send_message(client.user_id, f"{client.name}, вами была оформлена заявка №{application.id} "
                                                   f"на поставку:\n{product.abbreviation}   в количестве  "
                                                   f"{application.volume_declared} м3\n"
                                                   f"к {application.execution_time.strftime('%d.%m.%Y к %H:%M')}.\n")
            msg = await bot.send_message(client.user_id,
                                         f"Пожалуйста подтвердити готовность к разгрузки на строительной"
                                         f" площадки.\nПри необходимости вы сможете скорректировать время"
                                         f" подачи на следующем шаге после подтверждения",
                                         reply_markup=make_keyboard_by_list_only(["Подтвердить", "Отложить"]))
            print("msg.message_id = ", msg.message_id)
            state = dp.current_state(chat=client.user_id, user=client.user_id)
            await state.update_data(client=client)
            await state.update_data(application=application)
            await state.update_data(product=product)
            await state.update_data(the_object=the_object)
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(Reminder.waiting_for_approved)
            await asyncio.sleep(5)


# Принимает подтверждение. -> Запрашивает доп подтверждение времени
async def get_approve(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_data = await state.get_data()
    client = user_data["client"]
    application = user_data["application"]
    text = message.text
    time = application.execution_time
    if text == "Подтвердить":
        msg = await bot.send_message(client.user_id, f"Подтвердить готовность на "
                                                     f"{time.strftime('%H часов %M минут')}",
                                     reply_markup=dynamic_time(time))
        await state.update_data(msg=msg)
        # await state.update_data(msg_id=msg.message_id)
        await state.update_data(time=time)
        await state.set_state(Reminder.waiting_for_approved_time.state)
    else:
        await bot.send_message(client.user_id, f"{client.name}, в случае отсутствия готовности в заявленное время "
                                               f"вам необходимо незамедлительно отменить заявку или изменить "
                                               f"в ней время подачи!\nДля этого войдите в меню 'редактировать заявку'")
        await state.finish()


# Принимает  время подачи. ->   КОЛЛБЕКИ
# (Запрашивает количество)
async def get_time(callback_query: types.CallbackQuery, state: FSMContext):
    print("def get_time")
    user_id = callback_query.from_user.id
    # await del_old_message2(user_id, state)
    user_data = await state.get_data()
    time = user_data['time']
    product = user_data['product']
    now = datetime.datetime.now()
    if callback_query.data == 'now' and time > now:
        product = user_data['product']
        application = user_data['application']
        volume = application.volume_declared
        msg = await bot.send_message(user_id, f"Подтвердити готовность принять {product.product_type} в "
                                              f"количестве {volume} м3",
                                     reply_markup=dynamic_volume(volume))
        await state.update_data(msg_id=msg.message_id)
        await state.update_data(volume=volume)
        await state.set_state(Reminder.waiting_for_approved_volume.state)
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
        msg = user_data['msg']
        await msg.edit_text(f"Подтвердить готовность на "
                            f"{time.strftime('%H часов %M минут')}")
        await msg.edit_reply_markup(dynamic_time(time))



        # msg = await bot.send_message(user_id, f"Подтвердить готовность на "
        #                                       f"{time.strftime('%H часов %M минут')}",
        #                              reply_markup=dynamic_time(time))
        # await state.update_data(msg_id=msg.message_id)
        await state.set_state(Reminder.waiting_for_approved_time.state)


# Вспомогательная функция.  Сохраняет изменения в БД и оповещает об изменениях диспетчера
async def save_and_send_to_dispatcher(state: FSMContext):
    user_data = await state.get_data()
    application = user_data['application']
    client = user_data['client']
    product = user_data['product']
    the_object = user_data['the_object']
    time = user_data['time']
    volume = user_data['volume']
    application.volume_declared = volume
    application.execution_time = time
    application.is_executed = True
    application.save()
    await bot.send_message(client.user_id, f"Подтверждение принято. Ожидайте пожалуйста {product.product_type} "
                                           f"в назначенное время.")
    for dispatcher_id in active_dispatcher_id_list:
        await bot.send_message(dispatcher_id, emoji.emojize(":woman_raising_hand:"))
        await bot.send_message(dispatcher_id, f"Внимание, клиент подтвердил готовность по заявке №{application.id}\n"
                                              f"принять {product.product_type} в количестве "
                                              f"{application.volume_declared} м3 "
                                              f"в {application.execution_time.strftime('%H:%M')}\n"
                                              f"на объект '{the_object.obj_name}':")
        await pars_and_send_location(bot=bot, user_id=dispatcher_id, location=the_object.location)
    await state.finish()


# Принимает  объём. ->   КОЛЛБЕКИ
# Сохраняет изиенения в БД и оповещает об изменениях диспетчеру
async def get_volume(callback_query: types.CallbackQuery, state: FSMContext):
    print("def get_time")
    user_id = callback_query.from_user.id
    await del_old_message2(user_id, state)
    user_data = await state.get_data()
    volume = user_data['volume']
    product = user_data['product']
    if callback_query.data == 'send':
        await save_and_send_to_dispatcher(state)
    else:
        if callback_query.data == 'up':
            print("up")
            sign = 1
        else:
            print("down")
            sign = -1
        volume += sign * 0.5
        await state.update_data(volume=volume)
        msg = await bot.send_message(user_id, f"Подтвердити готовность принять {product.product_type} в "
                                              f"количестве {volume} м3",
                                     reply_markup=dynamic_volume(volume))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Reminder.waiting_for_approved_volume.state)


# Принимает  объём. ->   MESSAGE
# Сохраняет изменения в БД и оповещает об изменениях диспетчеру
async def get_volume2(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    volume = message.text
    try:
        volume = volume.replace(",", ".")
        await state.update_data(volume=float(volume))
        await save_and_send_to_dispatcher(state)
    except ValueError:
        msg = await bot.send_message(user_id, MessageApplication.request_volume_error)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Reminder.waiting_for_approved_volume.state)


def register_handlers_reminders(dp: Dispatcher):
    dp.register_message_handler(get_approve, state=Reminder.waiting_for_approved)
    dp.register_callback_query_handler(get_time, state=Reminder.waiting_for_approved_time)
    dp.register_callback_query_handler(get_volume, state=Reminder.waiting_for_approved_volume)
    dp.register_message_handler(get_volume2, state=Reminder.waiting_for_approved_volume)
