import datetime
from models import Client, Role, TheObject, Product, Driver, Dispatcher, Manager, Mixer, Application
from settings import LIST_ORGANIZATIONS_LINK
from with_file import download_from_yadisk, set_manager_id


# Принимает Класс + искомое -> возвращает соответствующие экземпляры класса
def set_list_instance_by_class_search(the_class, the_search):
    instance_list = []
    for instance in the_class.select().where((the_class.organization == the_search) & the_class.is_active):
        instance_list.append(instance)
    return instance_list


# Принимает Класс + искомое id-> возвращает соответствующий экземпляр класса (крайний)
def set_instance_by_class_and_id(the_class, user_id):
    instance_list = []
    for instance in the_class.select().where((the_class.user_id == user_id) & the_class.is_active):
        instance_list.append(instance)
    print('instance_list = ', instance_list)
    return instance_list[-1]


# Принимает Класс + искомое id-> возвращает соответствующий экземпляр класса (крайний)
def set_instance_by_class_and_id1(the_class, id_):
    instance_list = []
    for instance in the_class.select().where((the_class.id == id_) & the_class.is_active):
        instance_list.append(instance)
    print('instance_list = ', instance_list)
    return instance_list[-1]


# Принимает создателя > возвращает список его актуальных заявок для редактирования
def set_application_list_by_creator(creator: Client):
    instance_list = []
    for instance in Application.select().where((Application.creator == creator) & Application.is_active
                                               & (Application.is_executed == False) & (Application.is_delete == False)):
        instance_list.append(instance.id)
    print('instance_list = ', instance_list)
    return instance_list


# Возвращает список подтверждённых но не исполненных заявок
def set_executed_application_list():
    instance_list = []
    for instance in Application.select().where((Application.is_confirmation == False) & Application.is_active
                                               & Application.is_executed):
        instance_list.append(instance.id)
    print('instance_list = ', instance_list)
    return instance_list


# Возвращает список подтверждённых но не исполненных заявок по создателю
def set_executed_application_list_by_creator(creator: Client):
    instance_list = []
    for instance in Application.select().where((Application.creator == creator) & (Application.is_confirmation == False)
                                               & Application.is_executed & Application.is_active):
        instance_list.append(instance.id)
    print('instance_list = ', instance_list)
    return instance_list


# Возвращает список работающих но не занятых водителей
def set_free_driver_list():
    instance_list = []
    for instance in Driver.select().where(Driver.is_active & Driver.mixer.is_null(False)
                                          & Driver.working_by_application.is_null() & Driver.is_work):
        print('instance=', instance)
        print("instance.working_by_application = ", instance.working_by_application)
        print()
        mixer = instance.mixer
        instance_list.append(f"№{instance.id} {mixer.car_number} ({mixer.max_volume}) {instance.last_name}"
                             f" {instance.name}")

    print('instance_list = ', instance_list)
    return instance_list


# Возвращает список работающих по определённым заявкам водителей
def set_busy_driver_list_by_applications(applications: list[Application]):
    instance_list = []
    for instance in Driver.select().where(Driver.is_active & Driver.mixer.is_null(False)
                                          & (Driver.working_by_application in applications) & Driver.is_work):
        print('instance=', instance)
        print("instance.working_by_application = ", instance.working_by_application)
        print()
        mixer = instance.mixer
        instance_list.append(f"№{instance.id} {mixer.car_brand} {mixer.car_number}  {instance.name}")
    print('instance_list = ', instance_list)
    return instance_list


# Принимает создателя > возвращает список его актуальных заявок для удалени
def set_application_list_by_creator_for_del(creator: Client):
    instance_list = []
    for instance in Application.select().where((Application.creator == creator) & (Application.is_delete == False)
                                               & (Application.is_executed == False)):
        instance_list.append(instance.id)
    print('instance_list = ', instance_list)
    return instance_list


# Принимает дату > возвращает список  заявок на эту дату
def set_application_list_by_datetime(datetime_at: datetime):
    datetime_before = datetime_at + datetime.timedelta(days=1)
    instance_list = []
    for instance in Application.select().where((datetime_before > Application.execution_time > datetime_at)
                                               & Application.is_active
                                               & (Application.is_delete == False)).order_by(Application.execution_time):
        instance_list.append(instance)
    print('instance_list by datetime = ', instance_list)
    return instance_list


# Принимает Экземпляр Client-> возвращает список названия объектов
def set_theobject_by_client(instance_client, the_class=TheObject):
    object_name_list = []
    for instance in the_class.select().where((the_class.customer == instance_client) & the_class.is_active):
        object_name_list.append(instance.obj_name)
    print('object_name_list =  ', object_name_list)
    return object_name_list


# Принимает Экземпляр Client и название объекта-> возвращает экземпляр TheObject
def set_theobject_by_client_and_obj_name(instance_client, obj_name, the_class=TheObject):
    object_list = []
    for instance in the_class.select().where((the_class.customer == instance_client) & the_class.is_active &
                                             (the_class.obj_name == obj_name)):
        object_list.append(instance)
    print('object_name =  ', object_list)
    return object_list[-1]


# Принимает Экземпляр TheObject и абревиатуру продукта-> возвращает экземпляр Product
def set_product_by_theobject_and_abbr(instance_object, abbr, the_class=Product):
    product_list = []
    for instance in the_class.select().where((the_class.used_in == instance_object) & the_class.is_active &
                                             (the_class.abbreviation == abbr)):
        product_list.append(instance)
    print('product_list =  ', product_list)
    return product_list[-1]


# Принимает Экземпляр TheObject-> возвращает список абривиатур продукта
def set_product_by_object(instance_theobject, the_class=Product):
    product_abr_list = []
    for instance in the_class.select().where((the_class.used_in == instance_theobject) & the_class.is_active):
        product_abr_list.append(instance.abbreviation)
    print('product_abr_list =  ', product_abr_list)
    return product_abr_list


#  возвращает список Application до исполнения которых осталось меньше двух часов
def set_application_by_time(the_class=Application):
    now = datetime.datetime.now()
    timedelta = datetime.timedelta(hours=2, minutes=30)
    the_time = now + timedelta
    application_list = []

    for instance in the_class.select().where(
            (the_class.execution_time < the_time) & the_class.is_active & (the_class.is_executed != True)):
        application_list.append(instance)
    print('application_list =  ', application_list)
    return application_list


def set_car_number_by_organization(organization):
    car_numbers = []
    try:
        mixers = set_list_instance_by_class_search(Mixer, organization)
        for mixer in mixers:
            car_numbers.append(mixer.car_number)
        print('car_numbers = ', car_numbers)
    except Exception as err:
        print(err)
    return car_numbers


# Создаёт новый экземпляр класса Role
def add_new_Role(the_role):
    instance = Role(role=the_role)
    instance.save()
    return instance


# Создаёт новый экземпляр класса Client -> записывает в БД -> и возвращает его
def add_new_Client(user_id, name, last_name, phone, organization, post, photo, is_active=False):
    date_registration = datetime.date.today()
    src = download_from_yadisk(LIST_ORGANIZATIONS_LINK)
    manager_id = set_manager_id(src=src, organization=organization)  # Получаем manager_id с эксель файла
    manager = set_the_Manager_by_id(manager_id)  # Получаем экземпляр класса Manager
    instance = Client(
        is_active=is_active,
        date_registration=date_registration,
        user_id=user_id,
        name=name,
        last_name=last_name,
        phone=phone,
        organization=organization,
        person_manager=manager,
        post=post,
        photo=photo
    )
    instance.save()
    return instance


# Создаёт новый экземпляр класса Manager -> записывает в БД -> и возвращает его
def add_new_Manager(user_id, name, last_name, phone, photo, is_active=False):
    date_registration = datetime.date.today()
    instance = Manager(
        is_active=is_active,
        date_registration=date_registration,
        user_id=user_id,
        name=name,
        last_name=last_name,
        phone=phone,
        photo=photo
    )
    instance.save()
    return instance


# Создаёт новый экземпляр класса Dispatcher -> записывает в БД -> и возвращает его
def add_new_Dispatcher(user_id, name, last_name, phone, photo, is_active=False):
    date_registration = datetime.date.today()
    instance = Dispatcher(
        is_active=is_active,
        date_registration=date_registration,
        user_id=user_id,
        name=name,
        last_name=last_name,
        phone=phone,
        photo=photo
    )
    instance.save()
    return instance


# Создаёт новый экземпляр класса Driver -> записывает в БД -> и возвращает его
def add_new_Driver(user_id, name, last_name, phone, photo, organization, is_active=False):
    instance = Driver(
        is_active=is_active,
        date_registration=datetime.date.today(),
        user_id=user_id,
        name=name,
        last_name=last_name,
        organization=organization,
        phone=phone,
        photo=photo,
        is_work=False
    )
    instance.save()
    return instance


# Создаёт новый экземпляр класса Object -> записывает в БД -> и возвращает его
def add_new_Object(instance, obj_name, location=None):
    instance = TheObject(
        date_registration=datetime.date.today(),
        is_active=False,
        customer=instance,
        obj_name=obj_name,
        location=location
    )
    instance.save()
    return instance


# Создаёт новый экземпляр класса Mixer -> записывает в БД -> и возвращает его
def add_new_Mixer(organization, car_brand, car_number, max_volume, is_active=False, photo=None):
    instance = Mixer(
        date_registration=datetime.date.today(),
        is_active=is_active,
        organization=organization,
        car_brand=car_brand,
        car_number=car_number,
        max_volume=max_volume,
        photo=photo
    )
    instance.save()
    return instance


# Создаёт новый экземпляр класса Application -> записывает в БД -> и возвращает его
def add_new_Application(app_data):
    the_date = app_data['the_date']
    the_time = app_data['the_time']
    day = the_date.day
    month = the_date.month
    year = the_date.year

    hour = the_time.hour
    minute = the_time.minute

    new_date = datetime.datetime.strptime(f"{day}.{month}.{year} {hour}:{minute}", "%d.%m.%Y %H:%M")
    print(new_date)
    instance_client = app_data['instance_client']

    try:
        pump_sleeve_length = app_data['pump_sleeve_length']
        pump_feed_time = app_data['pump_feed_time']
        hour_p = pump_feed_time.hour
        minute_p = pump_feed_time.minute
        pump_feed_time = datetime.datetime.strptime(f"{day}.{month}.{year} {hour_p}:{minute_p}", "%d.%m.%Y %H:%M")
    except (KeyError, ValueError, IndexError):
        pump_sleeve_length = None
        pump_feed_time = None

    instance = Application(
        creation_time=datetime.datetime.now(),
        execution_time=new_date,
        is_delete=False,
        is_active=False,
        is_executed=False,
        is_confirmation=False,
        the_object=app_data['instance_theobject'],
        creator=instance_client,
        manager=instance_client.person_manager,
        product=app_data['instance_product'],
        volume_declared=app_data['volume_declared'],
        unloading_method=app_data['unloading_method'],
        declared_unloading_speed=app_data['declared_unloading_speed'],
        pump_sleeve_length=pump_sleeve_length,
        pump_feed_time=pump_feed_time,
    )
    instance.save()
    return instance


# Создаёт новый экземпляр класса Product -> записывает в БД -> и возвращает его
def add_new_Product(instance_theobject, product_type,
                    product_class=None,
                    frost_resistance=None,
                    water_permeability=None,
                    placeholder=None,
                    placeholder_fraction=None,
                    mobility=None,
                    cone_sediment=None,
                    mark_cement_mortal=None,
                    type_cement_mortal=None,
                    is_active=False):
    if product_class:
        abbreviation = f"{product_type} B{product_class} F{frost_resistance} W{water_permeability} П{mobility} " \
                       f"заполнитель: {placeholder} {placeholder_fraction}. Осадка конуса: {cone_sediment}"
    else:
        abbreviation = f"{product_type} Марки {mark_cement_mortal}  {type_cement_mortal}"
    instance = Product(
        date_registration=datetime.date.today(),
        is_active=is_active,
        product_type=product_type,
        product_class=product_class,
        frost_resistance=frost_resistance,
        water_permeability=water_permeability,
        placeholder=placeholder,
        placeholder_fraction=placeholder_fraction,
        mobility=mobility,
        cone_sediment=cone_sediment,
        mark_cement_mortal=mark_cement_mortal,
        type_cement_mortal=type_cement_mortal,
        used_in=instance_theobject,
        abbreviation=abbreviation
    )
    instance.save()
    return instance


# Возвращает экземпляр класса Role по заданному id
def set_the_Role_by_id(the_id):
    the_role = Role.get(id=the_id)
    return the_role


# Возвращает экземпляр класса TheObject по заданному id
def set_TheObject_by_id(the_id):
    the_object = TheObject.get(id=the_id)
    return the_object


# Возвращает экземпляр класса Manager по заданному id
def set_the_Manager_by_id(the_id):
    the_manager = Manager.get(id=the_id)
    return the_manager


# Возвращает экземпляр класса Client по заданному id
def set_the_Client_by_id(the_id):
    the_user = Client.get(id=the_id)
    return the_user


# Возвращает экземпляр класса Application по заданному id
def set_the_Application_by_id(the_id):
    application = Application.get(id=the_id)
    return application


# Возвращает экземпляр класса Mixer по заданному car_number
def set_the_Mixer_by_car_number(car_number):
    car = Mixer.get(car_number=car_number)
    return car


# Возвращает список экземпляров класса Role по значению role:
def set_the_Role_list_by_role(role):
    roles = [x for x in Role.select().where(Role.role == role)]
    return roles


# Удаляет экземпляр класса Client по заданному id
def del_the_Client_by_id(the_id):
    obj = Client.get(id=the_id)
    obj.delete_instance()
