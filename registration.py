import datetime
import random
import urllib.request

import emoji
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot import bot, TOKEN, dp
from keyboardsCollection import *
from message_text import MessageRegistration, ButtonRegistration
from settings import LIST_ORGANIZATIONS_LINK, LIST_TRANSPORT_ORGANIZATIONS_LINK, ADMIN_ID
from with_file import download_from_yadisk, set_list_organization
from with_db import *


class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_last_name = State()
    waiting_for_contact = State()
    waiting_for_role = State()
    waiting_for_organization = State()
    waiting_for_post = State()
    waiting_for_object = State()
    waiting_for_location = State()
    waiting_for_photo = State()
    approval_registration = State()
    waiting_for_car_brand = State()
    waiting_for_car_choice = State()
    waiting_for_car_number = State()
    waiting_for_max_volume = State()
    approval_registration_for_driver = State()


# Удаляет предидущее сообщение 2
async def del_old_message2(user_id, state: FSMContext):
    reg_data = await state.get_data()
    try:
        msg_id = reg_data["msg_id"]
        await bot.delete_message(chat_id=user_id, message_id=msg_id)
    except Exception as err:
        print(err)


# Удаляет предидущее сообщение
async def del_old_message(message: types.Message, state: FSMContext):
    reg_data = await state.get_data()
    try:
        msg_id = reg_data["msg_id"]
        await bot.delete_message(chat_id=message.from_user.id, message_id=msg_id)
    except Exception as err:
        print(err)


# Старт регистрации. Запрашивает имя
async def start_registration(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    print(f"{user_id}  in  async def start_registratio")
    await bot.send_message(user_id, emoji.emojize(":woman_technologist:"))
    msg = await bot.send_message(user_id, MessageRegistration.request_name, reply_markup=types.ReplyKeyboardRemove())
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Registration.waiting_for_name.state)


# Принимает имя. Запрашивает фамилию
async def get_name(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    name = message.text
    await state.update_data(name=name)
    msg = await bot.send_message(user_id, MessageRegistration.request_last_name)
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Registration.waiting_for_last_name.state)


# Принимает фамилию запрашивает контакт или телефон
async def get_last_name(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    last_name = message.text
    await state.update_data(last_name=last_name)
    msg = await bot.send_message(user_id, MessageRegistration.request_contact,
                                 reply_markup=make_keyboard_contact())
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Registration.waiting_for_contact.state)


# Принимает контакт запрашивает роль
async def get_contact(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    msg = await bot.send_message(user_id, MessageRegistration.request_role, reply_markup=make_keyboard_roles())
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Registration.waiting_for_role.state)


# Если контакт не отловлен принимает телефон и запрашивает роль
async def get_phone(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    phone = message.text
    await state.update_data(phone=phone)
    msg = await bot.send_message(user_id, MessageRegistration.request_role, reply_markup=make_keyboard_roles())
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Registration.waiting_for_role.state)


# Принимает роль. Запрашивает организацию
async def get_role(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    role = message.text
    if role not in ButtonRegistration.role_list:
        msg = await bot.send_message(user_id, MessageRegistration.request_role2, reply_markup=make_keyboard_roles())
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Registration.waiting_for_role.state)
    else:
        await state.update_data(role=role)
        if role == ButtonRegistration.role3 or role == ButtonRegistration.role2:  # *********  Менеджер или Диспетчер
            msg = await bot.send_message(user_id, MessageRegistration.request_photo,
                                         reply_markup=make_keyboard_send_later())
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(Registration.waiting_for_photo.state)
        else:  # ****************************************************************************   Клиент или водитель
            if role == ButtonRegistration.role1:  # *********  Водитель
                link = LIST_TRANSPORT_ORGANIZATIONS_LINK
            else:  # ****************************************  Клиент
                link = LIST_ORGANIZATIONS_LINK
            src = download_from_yadisk(link=link)  # Загрузка файла по ссылке с Яндекс диска на свой сервер
            list_organization = set_list_organization(src=src)  # Получение списка организаций из файла .xlsx
            await state.update_data(list_organization=list_organization)

            msg = await bot.send_message(user_id, MessageRegistration.request_organization,
                                         reply_markup=make_keyboard_by_list(list_organization))
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(Registration.waiting_for_organization.state)


# Принимает организацию запрашивает должность
async def get_organization(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    organization = message.text

    reg_data = await state.get_data()
    list_organization = reg_data["list_organization"]
    role = reg_data["role"]

    if organization not in list_organization:
        msg = await bot.send_message(user_id, MessageRegistration.request_organization2,
                                     reply_markup=make_keyboard_by_list(list_organization))
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Registration.waiting_for_organization.state)
    else:
        await state.update_data(organization=organization)
        if role == ButtonRegistration.role1:  # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     Водитель
            msg = await bot.send_message(user_id, MessageRegistration.request_photo,
                                         reply_markup=make_keyboard_send_later())
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(Registration.waiting_for_photo.state)

        else:  # Клиент
            msg = await bot.send_message(user_id, MessageRegistration.request_post)
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(Registration.waiting_for_post.state)


# Принимает должность запрашивает название объекта
async def get_post(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    post = message.text
    await state.update_data(post=post)
    msg = await bot.send_message(user_id, MessageRegistration.request_object)
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Registration.waiting_for_object.state)


# Принимает название объекта запрашивает геолокацию
async def get_object(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    the_object = message.text
    await state.update_data(the_object=the_object)
    msg = await bot.send_message(user_id, MessageRegistration.request_geolocation,
                                 reply_markup=make_keyboard_location())
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Registration.waiting_for_location.state)


# Принимает геолокацию запрашивает фото
async def get_location(message: types.Message, state: FSMContext):
    print("Heloo !!!!!!!!!!! from get_location")
    await del_old_message(message, state)
    user_id = message.from_user.id
    location = message.location
    await state.update_data(location=location)
    msg = await bot.send_message(user_id, MessageRegistration.request_photo, reply_markup=make_keyboard_send_later())
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Registration.waiting_for_photo.state)


# Принимает геолокацию2 (если геолокация не отправлена) запрашивает фото
async def get_location2(message: types.Message, state: FSMContext):
    print("Heloo !!!!!!!!!!! from get_location2222222222222")
    await del_old_message(message, state)
    user_id = message.from_user.id
    location = None
    await state.update_data(location=location)
    msg = await bot.send_message(user_id, MessageRegistration.request_photo, reply_markup=make_keyboard_send_later())
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Registration.waiting_for_photo.state)


# Принимает фото - завершает опрос - передаёт данные админу
async def get_photo(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    reg_data = await state.get_data()
    role = reg_data['role']
    try:
        make_topic_time = datetime.datetime.now() + datetime.timedelta(hours=3)  # Перевод в Московское время
        make_topic_time = make_topic_time.strftime('%Y_%m_%d-%H_%M')

        document_id = message.photo[-1].file_id
        file_info = await bot.get_file(document_id)
        fi = file_info.file_path

        src_new = f'data/userFiles/f__{make_topic_time}__{user_id}__{random.randrange(100)}.jpeg'
        src_new = src_new.replace(' ', '_')
        print('src_new= ', src_new)
        urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{TOKEN}/{fi}',
                                   src_new)
        await state.update_data(src_photo=src_new)
        print("src_photo= ", src_new)
    except Exception as err:
        print(err)
        reg_data = await state.get_data()
        role = reg_data['role']
        if role == ButtonRegistration.role2:
            print("*****************************")
            await state.update_data(src_photo='data/mainFiles/dispether.png')
        else:
            await state.update_data(src_photo='data/mainFiles/manager.png')
    reg_data = await state.get_data()
    role = reg_data['role']
    if not role == ButtonRegistration.role1:
        await bot.send_message(user_id, emoji.emojize(":woman_technologist:"))
        await bot.send_message(user_id, MessageRegistration.end)
    if role == ButtonRegistration.role0:  # ***********************************************************  Клиент
        instance = add_new_Client(  # записываем в БД и в переменную instance экземпляр класса   Клиент
            user_id=user_id,
            name=reg_data['name'],
            last_name=reg_data['last_name'],
            phone=reg_data['phone'],
            organization=reg_data['organization'],
            post=reg_data['post'],
            photo=reg_data['src_photo']
        )
        instance_Object = add_new_Object(
            instance=instance,
            obj_name=reg_data['the_object'],
            location=reg_data['location']
        )
        print("instance =  ", instance)
        print("instance.person_manager =  ", instance.person_manager)
        manager = instance.person_manager
        manager_id = manager.user_id
        await bot.send_message(manager_id, f"Получен запрос на регистрацию нового пользователя:")
        with open(reg_data['src_photo'], 'rb') as photo:
            await bot.send_photo(manager_id, photo)
        await bot.send_message(manager_id, f"id:      {user_id}\n"
                                           f"роль:    {reg_data['role']}\n"
                                           f"имя:     {reg_data['name']}\n"
                                           f"фамилия: {reg_data['last_name']}\n"
                                           f"телефон: {reg_data['phone']}\n"
                                           f"организация: {reg_data['organization']}\n"
                                           f"должность: {reg_data['post']}\n"
                               )
        location = reg_data['location']
        await bot.send_message(manager_id, f"Пользователь регестрирует объект:\n"
                                           f"   {reg_data['the_object']}"
                               )
        await bot.send_location(manager_id, location.latitude, location.longitude)
        msg = await bot.send_message(manager_id, ".", reply_markup=make_keyboard_approval_registration())
        await state.finish()

        the_state = dp.current_state(chat=manager_id, user=manager_id)
        await the_state.update_data(instance=instance)
        await the_state.update_data(instance_Object=instance_Object)
        await the_state.update_data(role=role)
        await the_state.update_data(msg_id=msg.message_id)
        await the_state.set_state(Registration.approval_registration)

    elif role == ButtonRegistration.role1:  # **********************************************************   Водитель
        instance = add_new_Driver(  # записываем в БД экземпляр класса Driver и в переменную instance
            user_id=user_id,
            name=reg_data['name'],
            last_name=reg_data['last_name'],
            phone=reg_data['phone'],
            organization=reg_data['organization'],
            photo=reg_data['src_photo']
        )
        await state.update_data(instance=instance)
        print("START")
        car_numbers = set_car_number_by_organization(reg_data['organization'])
        print("END")
        if car_numbers:
            await state.update_data(car_numbers=car_numbers)
            msg = await bot.send_message(user_id, MessageRegistration.request_car_choice,
                                         reply_markup=make_keyboard_by_list(car_numbers, "Добавить автомобиль"))
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(Registration.waiting_for_car_choice.state)

        else:
            msg = await bot.send_message(user_id, MessageRegistration.request_car_brand)
            await state.update_data(msg_id=msg.message_id)
            await state.set_state(Registration.waiting_for_car_brand.state)

    elif role == ButtonRegistration.role2 or role == ButtonRegistration.role3:

        if role == ButtonRegistration.role2:  # ***********************************************************  Диспетчер
            func = add_new_Dispatcher
        else:  # ******************************************************************************************* Менеджер
            func = add_new_Manager
        instance = func(  # записываем в БД экземпляр класса Manager и в переменную instance
            user_id=user_id,
            name=reg_data['name'],
            last_name=reg_data['last_name'],
            phone=reg_data['phone'],
            photo=reg_data['src_photo']
        )
        await bot.send_message(ADMIN_ID, f"Получен запрос на регистрацию нового пользователя:")
        with open(reg_data['src_photo'], 'rb') as photo:
            await bot.send_photo(ADMIN_ID, photo)
        await bot.send_message(ADMIN_ID, f"id:      {user_id}\n"
                                         f"роль:    {reg_data['role']}\n"
                                         f"имя:     {reg_data['name']}\n"
                                         f"фамилия: {reg_data['last_name']}\n"
                                         f"телефон: {reg_data['phone']}"
                               )
        msg = await bot.send_message(ADMIN_ID, ".", reply_markup=make_keyboard_approval_registration())
        await state.finish()

        the_state = dp.current_state(chat=ADMIN_ID, user=ADMIN_ID)
        await the_state.update_data(instance=instance)
        await the_state.update_data(role=role)
        await the_state.update_data(msg_id=msg.message_id)
        await the_state.set_state(Registration.approval_registration)


# Принимает подтверждения регестрации
async def get_approval_registration(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    reg_data = await state.get_data()
    instance = reg_data['instance']
    role = reg_data['role']
    try:
        if role == ButtonRegistration.role3 or role == ButtonRegistration.role2:  # Менеджер или Диспетчер
            if message.text == "Утвердить":
                instance.is_active = True
                instance.save()
                await bot.send_message(instance.user_id, f"Поздравляем {instance.name}.\n"
                                                         f"Ваша регистрация в приложении успешно завершена.\n")
                if role == ButtonRegistration.role3:
                    await bot.send_message(instance.user_id, f"Для идентификации в приложении вам как менеджеру "
                                                             f" присвоен номер (manager_id):  №{instance.id}")
            else:
                await bot.send_message(instance.user_id, f"Сожалею {instance.name}.\n"
                                                         f"Ваша регистрация отклонена")
        elif role == ButtonRegistration.role0:  # Клиент
            print("I am in  elif role == ButtonRegistration.role0:  # Клиент")
            if message.text == "Утвердить":
                instance_object = reg_data['instance_Object']
                instance.is_active = True
                instance.save()
                instance_object.is_active = True
                instance_object.save()
                await bot.send_message(instance.user_id, f"Поздравляем {instance.name}.\n"
                                                         f"Ваша регистрация в приложении успешно завершена.")
            else:
                await bot.send_message(instance.user_id, f"Сожалею {instance.name}.\n"
                                                         f"Ваша регистрация отклонена")
        await state.finish()
    except Exception as err:
        print(f"ОШИБКА в блоке обработки согласования нового юзера:  {err} ")


# Принимает выбранную машину и направляет запрос админу
async def get_choice_car(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    car_number = message.text

    reg_data = await state.get_data()
    car_numbers = reg_data["car_numbers"]

    if car_number not in car_numbers:
        msg = await bot.send_message(user_id, MessageRegistration.request_car_brand)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Registration.waiting_for_car_brand.state)
    else:
        await bot.send_message(user_id, MessageRegistration.end)
        mixer = set_the_Mixer_by_car_number(car_number)
        instance = reg_data['instance']
        instance.mixer_id = mixer
        instance.save()
        await bot.send_message(ADMIN_ID, f"Получен запрос на регистрацию нового пользователя:")
        with open(reg_data['src_photo'], 'rb') as photo:
            await bot.send_photo(ADMIN_ID, photo)
        await bot.send_message(ADMIN_ID,
                               f"id:      {user_id}\n"
                               f"роль:    {reg_data['role']}\n"
                               f"имя:     {reg_data['name']}\n"
                               f"фамилия: {reg_data['last_name']}\n"
                               f"телефон: {reg_data['phone']}\n"
                               f"организация: {reg_data['organization']}\n"
                               f"миксер:  {car_number}\n\n"
                               )
        msg = await bot.send_message(ADMIN_ID, ".", reply_markup=make_keyboard_approval_registration())
        await state.finish()

        the_state = dp.current_state(chat=ADMIN_ID, user=ADMIN_ID)
        await the_state.update_data(instance=instance)
        await the_state.update_data(instance_mixer=mixer)
        await the_state.update_data(msg_id=msg.message_id)
        await the_state.set_state(Registration.approval_registration_for_driver)


# Принимает марку машины -> запрашивает гос номер
async def get_car_brand(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    car_brand = message.text
    await state.update_data(car_brand=car_brand)
    msg = await bot.send_message(user_id, MessageRegistration.request_car_nubmer)
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Registration.waiting_for_car_number.state)


# Принимает номер машины -> запрашивает  максимальный объём бетона в миксере
async def get_car_number(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    car_number = message.text
    await state.update_data(car_number=car_number)
    msg = await bot.send_message(user_id, MessageRegistration.request_max_volume)
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Registration.waiting_for_max_volume.state)


# Принимает максимальный объём машины -> oтправляет данные на согласования админу
async def get_max_volume(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    user_id = message.from_user.id
    try:
        text = message.text.replace(',', '.')
        max_volume = float(text)
        reg_data = await state.get_data()
        await bot.send_message(user_id, MessageRegistration.end)
        mixer = add_new_Mixer(
            organization=reg_data['organization'],
            car_brand=reg_data['car_brand'],
            car_number=reg_data['car_number'],
            max_volume=max_volume,
        )

        await bot.send_message(ADMIN_ID, f"Получен запрос на регистрацию нового пользователя:")
        with open(reg_data['src_photo'], 'rb') as photo:
            await bot.send_photo(ADMIN_ID, photo)
        await bot.send_message(ADMIN_ID,
                               f"id:      {user_id}\n"
                               f"роль:    {reg_data['role']}\n"
                               f"имя:     {reg_data['name']}\n"
                               f"фамилия: {reg_data['last_name']}\n"
                               f"телефон: {reg_data['phone']}\n"
                               f"организация: {reg_data['organization']}\n"
                               )
        await bot.send_message(ADMIN_ID,
                               f"Пользователь хочет зарегестрировать машину:\n"
                               f"марка автомобиля:    {reg_data['car_brand']}\n"
                               f"гос номер:   {reg_data['car_number']}\n"
                               f"вместимость: {max_volume}м3\n"
                               )
        msg = await bot.send_message(ADMIN_ID, ".", reply_markup=make_keyboard_approval_registration())
        instance = reg_data['instance']
        await state.finish()

        the_state = dp.current_state(chat=ADMIN_ID, user=ADMIN_ID)
        await the_state.update_data(instance=instance)
        await the_state.update_data(instance_mixer=mixer)
        await the_state.update_data(msg_id=msg.message_id)
        await the_state.set_state(Registration.approval_registration_for_driver.state)

    except ValueError:
        msg = await bot.send_message(user_id, MessageRegistration.request_max_volume_error)
        await state.update_data(msg_id=msg.message_id)
        await state.set_state(Registration.waiting_for_max_volume.state)


# Принимает утверждения администратора от водителя
async def approval_registration_for_driver(message: types.Message, state: FSMContext):
    await del_old_message(message, state)
    reg_data = await state.get_data()
    instance, instance_mixer = [reg_data[x] for x in ("instance", "instance_mixer")]
    try:
        if message.text == "Утвердить":
            for the_instance in (instance, instance_mixer):
                the_instance.is_active = True
                the_instance.save()
            instance.mixer = instance_mixer
            instance.save()
            await bot.send_message(instance.user_id, f"Поздравляю {instance.name}.\n"
                                                     f"Ваша регистрация в приложении успешно завершена.\n")
        else:
            await bot.send_message(instance.user_id, f"Сожалею {instance.name}.\n"
                                                     f"Ваша регистрация отклонена")
        await state.finish()
    except Exception as err:
        print(f"ОШИБКА в блоке обработки согласования нового юзера:  {err} ")


def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(start_registration, commands="registration", state="*")
    dp.register_message_handler(get_name, state=Registration.waiting_for_name)
    dp.register_message_handler(get_last_name, state=Registration.waiting_for_last_name)
    dp.register_message_handler(get_contact,
                                state=Registration.waiting_for_contact,
                                content_types=types.ContentType.CONTACT)
    dp.register_message_handler(get_phone, state=Registration.waiting_for_contact)
    dp.register_message_handler(get_role, state=Registration.waiting_for_role)
    dp.register_message_handler(get_organization, state=Registration.waiting_for_organization)
    dp.register_message_handler(get_post, state=Registration.waiting_for_post)
    dp.register_message_handler(get_object, state=Registration.waiting_for_object)
    dp.register_message_handler(get_location,
                                state=Registration.waiting_for_location,
                                content_types=types.ContentType.LOCATION)
    dp.register_message_handler(get_location2, state=Registration.waiting_for_location)
    dp.register_message_handler(get_photo,
                                state=Registration.waiting_for_photo,
                                content_types=types.ContentTypes.ANY)
    dp.register_message_handler(get_approval_registration, state=Registration.approval_registration)
    dp.register_message_handler(get_choice_car, state=Registration.waiting_for_car_choice)
    dp.register_message_handler(get_car_brand, state=Registration.waiting_for_car_brand)
    dp.register_message_handler(get_car_number, state=Registration.waiting_for_car_number)
    dp.register_message_handler(get_max_volume, state=Registration.waiting_for_max_volume)
    dp.register_message_handler(approval_registration_for_driver, state=Registration.approval_registration_for_driver)
