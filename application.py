import datetime
import random
import urllib.request

import emoji
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot import bot, TOKEN, dp
from keyboardsCollection import *
from message_text import *
from with_db import *
from registration import del_old_message, del_old_message2
from inlineKeyboards import dynamic_keyboard
from with_handler import pars_and_send_location


class Application(StatesGroup):
    waiting_for_execution_date = State()
    waiting_for_execution_time = State()
    waiting_for_the_object = State()
    waiting_for_product = State()
    waiting_for_volume_declared = State()
    waiting_for_unloading_method = State()
    waiting_for_declared_unloading_speed = State()
    waiting_for_pump_sleeve_length = State()
    waiting_for_pump_feed_time = State()

    waiting_for_object_name = State()
    waiting_for_location = State()

    waiting_for_product_type = State()
    waiting_for_product_class = State()
    waiting_for_frost_resistance = State()
    waiting_for_water_permeability = State()
    waiting_for_placeholder = State()
    waiting_for_placeholder_fraction = State()
    waiting_for_mobility = State()
    waiting_for_cone_sediment = State()

    waiting_for_mark_cement_mortal = State()
    waiting_for_type_cement_mortal = State()

    waiting_for_approval = State()


# Принимает  тип продукта. -> Запрашивает класс бетона
async def get_product_type(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    product_type = message.text
    if product_type in ButtonProduct.product_list:
        await state.update_data(product_type=product_type)
        if product_type == ButtonProduct.product_list[1]:
            msg = await bot.send_message(user_id, MessageProduct.request_class)
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(Application.waiting_for_product_class.state)
        else:
            msg = await bot.send_message(user_id, MessageProduct.request_mark_cement_mortal)
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(Application.waiting_for_mark_cement_mortal.state)
    else:
        msg = await bot.send_message(user_id, MessageProduct.request_type_error,
                                     reply_markup=make_keyboard_by_list(ButtonProduct.product_list))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_product_type.state)


# Принимает  класс бетона. -> Запрашивает марку по морозостойкости
async def get_product_class(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    product_class = message.text
    try:
        await state.update_data(product_class=float(product_class))
        msg = await bot.send_message(user_id, MessageProduct.request_frost_resistance)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_frost_resistance.state)
    except ValueError:
        msg = await bot.send_message(user_id, MessageProduct.request_class_error)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_product_class.state)


# Принимает  марку по морозостойкости. -> Запрашивает показатель проницаемости водой
async def get_frost_resistance(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    frost = message.text
    try:
        await state.update_data(frost=int(frost))
        msg = await bot.send_message(user_id, MessageProduct.request_water_permeability)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_water_permeability.state)
    except ValueError:
        msg = await bot.send_message(user_id, MessageProduct.request_frost_resistance_error)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_frost_resistance.state)


# Принимает  показатель проницаемости водой. -> Запрашивает заполнитель
async def get_water_permeability(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    water = message.text
    try:
        await state.update_data(water=int(water))
        msg = await bot.send_message(user_id, MessageProduct.request_placeholder,
                                     reply_markup=make_keyboard_by_list(ButtonProduct.placeholder_list))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_placeholder.state)
    except ValueError:
        msg = await bot.send_message(user_id, MessageProduct.request_water_permeability_error)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_water_permeability.state)


# Принимает  заполнитель. -> Запрашивает фракцию заполнителя
async def get_placeholder(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    placeholder = message.text
    if placeholder in ButtonProduct.placeholder_list:
        await state.update_data(placeholder=placeholder)
        msg = await bot.send_message(user_id, MessageProduct.request_placeholder_fraction,
                                     reply_markup=make_keyboard_by_list(ButtonProduct.fractions_list))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_placeholder_fraction.state)
    else:
        msg = await bot.send_message(user_id, MessageProduct.request_placeholder_error,
                                     reply_markup=make_keyboard_by_list(ButtonProduct.placeholder_list))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_placeholder.state)


# Принимает фракцию заполнителя. -> Запрашивает марку по удобоукладываемости
async def get_placeholder_fraction(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    placeholder_fraction = message.text
    if placeholder_fraction in ButtonProduct.fractions_list:
        await state.update_data(placeholder_fraction=placeholder_fraction)
        msg = await bot.send_message(user_id, MessageProduct.request_mobility)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_mobility.state)
    else:
        msg = await bot.send_message(user_id, MessageProduct.request_placeholder_fraction_error,
                                     reply_markup=make_keyboard_by_list(ButtonProduct.fractions_list))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_placeholder_fraction.state)


# Принимает  марку по удобоукладываемости. -> Запрашивает осадку конуса
async def get_mobility(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    mobility = message.text
    try:
        await state.update_data(mobility=int(mobility))
        msg = await bot.send_message(user_id, MessageProduct.request_cone_sediment)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_cone_sediment.state)
    except ValueError:
        msg = await bot.send_message(user_id, MessageProduct.request_mobility)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_mobility.state)


# Принимает осадку конуса. -> Создаёт в БД экземпляр класса Product ->
async def get_cone_sediment(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    cone_sediment = message.text
    await state.update_data(cone_sediment=cone_sediment)
    app_data = await state.get_data()
    instance_product = add_new_Product(
        instance_theobject=app_data['instance_theobject'],
        product_type=app_data['product_type'],
        product_class=app_data['product_class'],
        frost_resistance=app_data['frost'],
        water_permeability=app_data['water'],
        placeholder=app_data['placeholder'],
        placeholder_fraction=app_data['placeholder_fraction'],
        mobility=app_data['mobility'],
        cone_sediment=cone_sediment
    )
    await state.update_data(instance_product=instance_product)
    msg = await bot.send_message(user_id, MessageApplication.request_volume)
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Application.waiting_for_volume_declared.state)


# Принимает  марку раствора. -> Запрашивает тип раствора
async def get_mark_cement_mortal(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    mark_cement_mortal = message.text
    try:
        await state.update_data(mark_cement_mortal=int(mark_cement_mortal))
        msg = await bot.send_message(user_id, MessageProduct.request_type_cement_mortal,
                                     reply_markup=make_keyboard_by_list(ButtonProduct.type_cement_mortal_list))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_type_cement_mortal.state)
    except ValueError:
        msg = await bot.send_message(user_id, MessageProduct.request_mark_cement_mortal_error)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_mark_cement_mortal.state)


# Принимает тип раствора. -> Сохраняет экземпляр Product в БД -> Запрашивает объём
async def get_type_cement_mortal(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    type_cement_mortal = message.text
    if type_cement_mortal in ButtonProduct.type_cement_mortal_list:
        await state.update_data(type_cement_mortal=type_cement_mortal)
        app_data = await state.get_data()
        instance_product = add_new_Product(
            instance_theobject=app_data['instance_theobject'],
            product_type=app_data['product_type'],
            mark_cement_mortal=app_data['mark_cement_mortal'],
            type_cement_mortal=type_cement_mortal,
        )
        await state.update_data(instance_product=instance_product)
        msg = await bot.send_message(user_id, MessageApplication.request_volume)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_volume_declared.state)
    else:
        msg = await bot.send_message(user_id, MessageProduct.request_type_cement_mortal_error,
                                     reply_markup=make_keyboard_by_list(ButtonProduct.type_cement_mortal_list))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_type_cement_mortal.state)


# Принимает название объекта запрашивает геолокацию
async def get_object_name(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    object_name = message.text
    await state.update_data(object_name=object_name)
    await state.update_data(instance_theobject=None)
    msg = await bot.send_message(user_id, MessageRegistration.request_geolocation,
                                 reply_markup=make_keyboard_location())
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Application.waiting_for_location.state)


# Принимает геолокацию -> Регестрирует новый объект -> Запрашивает тип продукции (Бетон или Раствор)
async def get_location(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    location = message.location
    await state.update_data(location=location)
    app_data = await state.get_data()
    instance_theobject = app_data['instance_theobject']
    if not instance_theobject:
        instance_theobject = add_new_Object(
            instance=app_data['instance_client'],
            obj_name=app_data['object_name'],
            location=app_data['location']
        )
        await state.update_data(instance_theobject=instance_theobject)
    else:
        instance_theobject.location = location
        instance_theobject.save()
    msg = await bot.send_message(user_id, MessageProduct.request_type,
                                 reply_markup=make_keyboard_by_list(ButtonProduct.product_list))
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Application.waiting_for_product_type.state)


# Принимает геолокацию2 (если геолокация не отправлена)
async def get_location2(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    msg = await bot.send_message(user_id, MessageRegistration.request_geolocation_error,
                                 reply_markup=make_keyboard_location())
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Application.waiting_for_location.state)


# Старт оформления заявки. -> Проверяет id на принадлежность к Client -> Запрашивает на какую дату
async def start_application(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    print(f"{user_id}  in  async def start_application")
    try:
        instance_client = set_instance_by_class_and_id(Client, user_id)
        await bot.send_message(user_id, emoji.emojize(":woman_technologist:"))
        print('instance_client.name =  ', instance_client.name)
        await bot.send_message(user_id, f'Здравствуйте, {instance_client.name}')
        await state.update_data(instance_client=instance_client)
        msg = await bot.send_message(user_id, MessageApplication.request_date,
                                     reply_markup=make_keyboard_by_list(ButtonApplication.date_list,
                                                                        ButtonApplication.today))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_execution_date.state)
    except (ValueError, IndexError):
        await bot.send_message(user_id, MessageApplication.start_error)


# Принимает  дату. -> Запрашивает время
async def get_date(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    text = message.text
    try:
        if text == ButtonApplication.date_list[0]:
            the_date = datetime.date.today() + datetime.timedelta(days=1)
        elif text == ButtonApplication.date_list[1]:
            the_date = datetime.date.today() + datetime.timedelta(days=2)
        elif text == ButtonApplication.today:
            the_date = datetime.date.today()
        else:
            the_date = datetime.datetime.strptime(text, "%d.%m.%Y")
            print('the_date = ', the_date)
        await state.update_data(the_date=the_date)
        msg = await bot.send_message(user_id, MessageApplication.request_time)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_execution_time.state)
    except ValueError:
        msg = await bot.send_message(user_id, MessageApplication.request_date_error)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_execution_date.state)


# Принимает  время. -> Запрашивает выбрать объект
async def get_time(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    text = message.text
    try:
        the_time = datetime.datetime.strptime(text, "%H:%M")
        print('the_time = ', the_time)
        await state.update_data(the_time=the_time)
        app_data = await state.get_data()
        object_name_list = set_theobject_by_client(app_data['instance_client'])
        msg = await bot.send_message(user_id, MessageApplication.request_object_choice,
                                     reply_markup=make_keyboard_by_list(object_name_list, ButtonApplication.add_object))
        await state.update_data(msg_id=msg.message_id)
        await state.update_data(object_name_list=object_name_list)
        await state.set_state(Application.waiting_for_the_object.state)
    except ValueError:
        msg = await bot.send_message(user_id, MessageApplication.request_time_error)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_execution_time.state)


# Принимает выбор объекта. -> Запрашивает продукт
async def get_object_choice(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    text = message.text
    app_data = await state.get_data()
    if text == ButtonApplication.add_object:
        msg = await bot.send_message(user_id, MessageRegistration.request_object)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_object_name.state)
    elif text in app_data['object_name_list']:
        print('i am in:    elif text in app_data[object_name_list]')
        instance_theobject = set_theobject_by_client_and_obj_name(app_data['instance_client'], text)
        await state.update_data(instance_theobject=instance_theobject)
        if not instance_theobject.location:
            msg = await bot.send_message(user_id, MessageRegistration.request_geolocation,
                                         reply_markup=make_keyboard_location())
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(Application.waiting_for_location.state)
        else:
            product_abbr_list = set_product_by_object(instance_theobject)
            if product_abbr_list:
                print("i am in:  if product_abbr_list: ")
                msg = await bot.send_message(user_id, MessageApplication.request_product,
                                             reply_markup=make_keyboard_by_list(product_abbr_list))
                await state.update_data(msg_id=msg.message_id)
                await state.update_data(product_abbr_list=product_abbr_list)
                await state.set_state(Application.waiting_for_product.state)
            else:
                msg = await bot.send_message(user_id, MessageProduct.request_type,
                                             reply_markup=make_keyboard_by_list(ButtonProduct.product_list))
                await state.update_data(msg_id=msg.message_id)
                await state.set_state(Application.waiting_for_product_type.state)
    else:
        msg = await bot.send_message(user_id, MessageProduct.error1,
                                     reply_markup=make_keyboard_by_list(app_data['object_name_list'],
                                                                        ButtonApplication.add_object))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_the_object.state)


# Принимает выбор продукта. -> Запрашивает объём
async def get_product_choice(message: types.Message, state: FSMContext):
    print("I am in   def get_product_choice (# Принимает выбор продукта. -> Запрашивает объём)")
    await del_old_message(message, state)
    user_id = message.from_user.id
    text = message.text
    app_data = await state.get_data()
    if text not in app_data['product_abbr_list']:
        msg = await bot.send_message(user_id, MessageProduct.request_type,
                                     reply_markup=make_keyboard_by_list(ButtonProduct.product_list))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_product_type.state)
    else:
        instance_product = set_product_by_theobject_and_abbr(app_data['instance_theobject'], text)
        print("instance_product = ", instance_product)
        await state.update_data(instance_product=instance_product)
        msg = await bot.send_message(user_id, MessageApplication.request_volume)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_volume_declared.state)


# Принимает  объём. -> Запрашивает метод разгрузки
async def get_volume(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    volume = message.text
    try:
        await state.update_data(volume_declared=float(volume))
        msg = await bot.send_message(user_id, MessageApplication.request_unloading_method,
                                     reply_markup=make_keyboard_by_list(ButtonApplication.unloading_method_list))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_unloading_method.state)
    except ValueError:
        msg = await bot.send_message(user_id, MessageApplication.request_volume)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_volume_declared.state)


# Принимает  метод разгрузки. -> Запрашивает скорость разгрузки куб/час
async def get_unloading_method(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    unloading_method = message.text
    if unloading_method in ButtonApplication.unloading_method_list:
        await state.update_data(unloading_method=unloading_method)
        app_data = await state.get_data()
        instance_theobject = app_data['instance_theobject']
        if unloading_method == ButtonApplication.unloading_method_list[1]:
            speed = instance_theobject.average_speed_of_unloading_by_pump or 30.0
        elif unloading_method == ButtonApplication.unloading_method_list[0]:
            speed = instance_theobject.average_speed_of_unloading_by_crane or 7.0
        else:
            speed = instance_theobject.average_speed_of_unloading_by_self_watering or 20.0
        await state.update_data(speed=speed)
        await bot.send_message(user_id, emoji.emojize(":woman_technologist:"))
        await bot.send_message(user_id, f"Давайте определимся с интервалом отправки машин."
                                        f"Средняя скорость разгрузки данным способом на вашем объекте составляет "
                                        f"{speed} кубов в час")
        msg = await bot.send_message(user_id, f"Расчитать интервал из расчёта "
                                              f"{speed} кубов в час",
                                     reply_markup=dynamic_keyboard(speed))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_declared_unloading_speed.state)
    else:
        msg = await bot.send_message(user_id, MessageProduct.error1,
                                     reply_markup=make_keyboard_by_list(ButtonApplication.unloading_method_list))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_unloading_method.state)


# Вспомогательная функция (Записывает Application в БД -> Отправляет заявку менеджеру)
async def record_data_and_send_request_to_manager(state: FSMContext, user_id):
    app_data = await state.get_data()
    await bot.send_message(user_id, emoji.emojize(":woman_technologist:"))
    app_data = await state.get_data()
    application = add_new_Application(app_data)
    await state.update_data(instance_application=application)
    await bot.send_message(user_id, do_end(application))

    client = app_data['instance_client']
    product = app_data['instance_product']
    manager = client.person_manager
    theobject = app_data['instance_theobject']
    manager_id = manager.user_id

    with open(client.photo, 'rb') as photo:
        await bot.send_photo(manager_id, photo)
    await bot.send_message(manager_id, f"Клиент {client.name} {client.last_name},\n"
                                       f"{client.post}  {client.organization}\nсделал заявку "
                                       f" №{application.id}:\n"
                                       f"на {application.execution_time.strftime('%d.%m.%Y к %H:%M')}\n"
                                       f"{product.abbreviation}\n"
                                       f"в количестве:  {application.volume_declared}м3\n"
                                       f"метод разгрузки:   {application.unloading_method}\n"
                                       f"на объект '{theobject.obj_name}'\n"
                           )
    await pars_and_send_location(bot, theobject.location, manager_id)
    if application.pump_feed_time:
        await bot.send_message(manager_id, f"Клиент запрашивает бетононасос длиной {application.pump_sleeve_length} "
                                           f"метров\n"
                                           f"на {application.pump_feed_time.strftime('%d.%m.%Y к %H:%M')}\n")
    msg = await bot.send_message(manager_id,
                                 "Пожалуйста нажмите на кнопку 'Согласовать' или пришлите мне причину отказа",
                                 reply_markup=make_keyboard_approval())
    await state.finish()
    the_state = dp.current_state(chat=manager_id, user=manager_id)
    await the_state.update_data(client=client)
    await the_state.update_data(theobject=theobject)
    await the_state.update_data(product=product)
    await the_state.update_data(application=application)
    await the_state.update_data(msg_id=msg.message_id)
    await the_state.set_state(Application.waiting_for_approval)


# Принимает  скорость разгрузки. ->   КОЛЛБЕКИ
# (Запрашивает длину стрелы бетононасоса)    или   (Записывает Application в БД -> Отправляет заявку менеджеру)
async def new_test(callback_query: types.CallbackQuery, state: FSMContext):
    print("async def new_test(callback_query: types.CallbackQuery, state: FSMContext)")
    user_id = callback_query.from_user.id
    await del_old_message2(user_id, state)
    app_data = await state.get_data()
    if app_data['unloading_method'] == ButtonApplication.unloading_method_list[1]:
        step = 5
    else:
        step = 0.5
    speed = app_data['speed']
    if callback_query.data == 'send':
        await state.update_data(declared_unloading_speed=speed)
        if app_data['unloading_method'] == ButtonApplication.unloading_method_list[1]:
            msg = await bot.send_message(user_id, MessageApplication.request_pump_sleeve_length)
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(Application.waiting_for_pump_sleeve_length.state)
        else:
            await record_data_and_send_request_to_manager(state, user_id)
    elif callback_query.data == 'up':
        print("up")
        speed += step
        await state.update_data(speed=speed)
        msg = await bot.send_message(user_id, f"Расчитать интервал из расчёта "
                                              f"{speed} кубов в час",
                                     reply_markup=dynamic_keyboard(speed))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_declared_unloading_speed.state)
    elif callback_query.data == 'down':
        print("NO")
        speed -= step
        await state.update_data(speed=speed)
        msg = await bot.send_message(user_id, f"Расчитать интервал из расчёта "
                                              f"{speed} кубов в час",
                                     reply_markup=dynamic_keyboard(speed))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_new.state)


# Принимает  скорость разгрузки. ->
# (Запрашивает длину стрелы бетононасоса)    или   (Записывает Product в БД -> Отправляет заявку менеджеру)
async def get_speed(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    speed = message.text
    try:
        await state.update_data(declared_unloading_speed=float(speed))
        app_data = await state.get_data()
        if app_data['unloading_method'] == ButtonApplication.unloading_method_list[1]:
            msg = await bot.send_message(user_id, MessageApplication.request_pump_sleeve_length)
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(Application.waiting_for_pump_sleeve_length.state)
        else:
            await record_data_and_send_request_to_manager(state, user_id)
    except ValueError:
        msg = await bot.send_message(user_id, MessageApplication.request_unloading_speed_error)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_declared_unloading_speed.state)


# Принимает  длину стрелы. -> Запрашивает время подачи бетононасоса
async def get_pump_sleeve_length(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    length = message.text
    try:
        await state.update_data(pump_sleeve_length=float(length))
        msg = await bot.send_message(user_id, MessageApplication.request_pump_feed_time)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_pump_feed_time.state)
    except ValueError:
        msg = await bot.send_message(user_id, MessageApplication.request_pump_sleeve_length_error)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_pump_sleeve_length.state)


# Принимает  время подачи бетононасоса. -> Записывает Application в БД -> Отправляет заявку менеджеру
async def get_pump_feed_time(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    text = message.text
    try:
        the_time = datetime.datetime.strptime(text, "%H:%M")
        print('the_time = ', the_time)
        await state.update_data(pump_feed_time=the_time)
        await record_data_and_send_request_to_manager(state, user_id)
    except ValueError:
        msg = await bot.send_message(user_id, MessageApplication.request_time_error)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Application.waiting_for_execution_time.state)


# Принимает согласование заявки от менеджера
async def approval_application(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    app_data = await state.get_data()
    client, product, theobject, application = [app_data[x] for x in ("client", "product", "theobject", "application")]
    try:
        if application.is_delete:
            manager = client.person_manager
            await bot.send_message(manager.user_id,
                                   "Заявка не может быть согласована так как ранее была удалена клиентом")
        else:
            if message.text == "Согласовать":
                for the_instance in (product, application):
                    the_instance.is_active = True
                    the_instance.save()
                    application.visa_time = datetime.datetime.now()
                await bot.send_message(client.user_id, do_answer_about_approve(client, application))
            else:
                await bot.send_message(client.user_id, do_rejection_about_approve(client, application, message.text))
        await state.finish()
    except Exception as err:
        print(f"ОШИБКА в блоке обработки согласования заявки:  {err} ")


def register_handlers_application(dp: Dispatcher):
    dp.register_message_handler(get_product_type, state=Application.waiting_for_product_type)
    dp.register_message_handler(get_product_class, state=Application.waiting_for_product_class)
    dp.register_message_handler(get_frost_resistance, state=Application.waiting_for_frost_resistance)
    dp.register_message_handler(get_water_permeability, state=Application.waiting_for_water_permeability)
    dp.register_message_handler(get_placeholder, state=Application.waiting_for_placeholder)
    dp.register_message_handler(get_placeholder_fraction, state=Application.waiting_for_placeholder_fraction)
    dp.register_message_handler(get_mobility, state=Application.waiting_for_mobility)
    dp.register_message_handler(get_cone_sediment, state=Application.waiting_for_cone_sediment)

    dp.register_message_handler(get_mark_cement_mortal, state=Application.waiting_for_mark_cement_mortal)
    dp.register_message_handler(get_type_cement_mortal, state=Application.waiting_for_type_cement_mortal)

    dp.register_message_handler(get_object_name, state=Application.waiting_for_object_name)
    dp.register_message_handler(get_location, state=Application.waiting_for_location,
                                content_types=types.ContentType.LOCATION)
    dp.register_message_handler(get_location2, state=Application.waiting_for_location)

    dp.register_message_handler(start_application, commands="application", state="*")
    dp.register_message_handler(get_date, state=Application.waiting_for_execution_date)
    dp.register_message_handler(get_time, state=Application.waiting_for_execution_time)
    dp.register_message_handler(get_object_choice, state=Application.waiting_for_the_object)
    dp.register_message_handler(get_product_choice, state=Application.waiting_for_product)
    dp.register_message_handler(get_volume, state=Application.waiting_for_volume_declared)
    dp.register_message_handler(get_unloading_method, state=Application.waiting_for_unloading_method)
    dp.register_callback_query_handler(new_test, state=Application.waiting_for_declared_unloading_speed)
    dp.register_message_handler(get_speed, state=Application.waiting_for_declared_unloading_speed)
    dp.register_message_handler(get_pump_sleeve_length, state=Application.waiting_for_pump_sleeve_length)
    dp.register_message_handler(get_pump_feed_time, state=Application.waiting_for_pump_feed_time)
    dp.register_message_handler(approval_application, state=Application.waiting_for_approval)
