from aiogram.dispatcher import FSMContext


class ButtonRegistration:
    request_contact = "Отправить контакт"
    request_location = "Отправить геолокацию"
    send_later = "Отправить позже"
    role_list = ["Клиент РБУ", "Водитель миксера", "Диспетчер", "Менеджер"]
    role0 = role_list[0]
    role1 = role_list[1]
    role2 = role_list[2]
    role3 = role_list[3]


class ButtonProduct:
    product_list = ['Раствор', 'Бетон']
    placeholder_list = ['Гравийный щебень', 'Гранитный щебень']
    fractions_list = ['Фракция щебня 5 - 20мм',
                      'Мелкозернистый бетон с фракцией до 5мм']
    type_cement_mortal_list = ['Кладочный', 'Для стяжки пола']


class ButtonApplication:
    date_list = ['На ЗАВТРА', 'На ПОСЛЕЗАВТРА']
    today = 'На СЕГОДНЯ!!'
    add_object = 'Добавить новый объект'
    unloading_method_list = ["Подъёмным краном", "Бетононасосом", "Самосливом"]


class ButtonRedact:
    actions_list = ["Подтвердить готовность", "Изменить время", "Изменить количество", "Изменить интервал отггрузки"]


class MessageRegistration:
    request_name = "Отлично!! Давайте пройдём процедуру регистрации.\n" \
                   "Для начала пришлите мне Ваше имя"

    request_last_name = "Пришлите мне фамилию"

    request_contact = f"Теперь отправте мне номер телефона по которому с вами можно будет всегда связаться.\n" \
                      f"Если это тот же номер по которому вы зарегестрированы в мессенджере 'Telegram' " \
                      f"просто нажмите на кнопку {ButtonRegistration.request_contact} "

    request_role = "Выберите из предложенных вариантов вашу роль в приложении"

    request_role2 = "К сожалению такой роли пока нету - выберите из предложенных вариантов"

    request_organization = "Отлично. Теперь напишите мне название Вашей организации"

    request_organization2 = "К сожалению других зарегестрированных в приложении организаций пока нет.\nПожалуйста" \
                            "выберите из списка или обратитесь за помощью к вашему персональному менеджеру"

    request_post = "Отлично.\nНужна ещё Ваша должность в ней"

    request_object = " " \
                     "Отправте мне название объекта куда нужно будет доставить продукцию"

    request_geolocation = f"Теперь мне нужна геолокация этого объекта. Если вы в данный момент находитись " \
                          f"там - просто убедитись, что на Вашем смартфоне включено определение геололкации " \
                          f"и нажмите на кнопку {ButtonRegistration.request_location}"

    request_geolocation_error = f'Для того чтобы оформить заявку на объект нужна его геолокация'

    request_photo = "Ok\nПришлите мне ещё фото для Вашей аватарки в приложении"

    request_car_brand = "Пришлите мне название марки автомобиля (миксера)"

    request_car_choice = "Выберите машину на которой будете работать:"

    request_car_nubmer = "Введите гос номер автомобиля"

    request_max_volume = "Введите максимальную вместимость бетонной транспортной смеси в метрах кубических"

    request_max_volume_error = "Вместимость должна быть числом. Например если вместимость составляет девять с" \
                               " половиной кубов -> введите число: 9,5"

    end = "Хорошо. Я записала все Ваши данные и отправила на обработку.\n" \
          "Через некоторое время Вам придёт уведомление с подтверждением регистрации.\n" \
          "Не забудте включить звук для уведомлений этого чата"


class MessageProduct:
    error1 = 'К сожалению можем предложить вам выбрать только это.\n' \
             'Пожалуйста попробуйте ещё раз выбрать из списка:'

    request_mark_cement_mortal = 'Пришлите мне требуемую марку раствора'

    request_mark_cement_mortal_error = 'Это должно быть число.\nНапример если вам требуется раствор марки 100' \
                                       ' -> пришлите мне число 100'

    request_type_cement_mortal = 'Выберите вид раствора:'

    request_type_cement_mortal_error = error1

    request_type = 'Выберите какой тип продукции вам нужен'

    request_type_error = error1

    request_class = 'Пришлите марку В'

    request_class_error = 'Это должно быть число - например если вам нужен бетон класса В25 -> введите 25'

    request_frost_resistance = 'Пришлите мне показатель морозостойкости  F'

    request_frost_resistance_error = 'Это должно быть число - например если вам нужyно F100 -> введите 100'

    request_water_permeability = 'Введити показатель проницаемости водой  W'

    request_water_permeability_error = 'Это должно быть числом - например если вам нужно W4 -> просто введити 4'

    request_placeholder = 'На каком заполнитили вам нужен бетон - выберити из предложенных вариантов:'

    request_placeholder_error = error1

    request_placeholder_fraction = 'Выберити необходимую фракцию щебня'

    request_placeholder_fraction_error = error1

    request_mobility = 'Пришлите мне марку по удобоукладываемости  П'

    request_mobility_error = 'Это должно быть числом - например если вам нужно П4 -> просто введити 4'

    request_cone_sediment = 'Пришлите требуемую осадку конуса - например для П4 она составляет 16-20см '


class MessageApplication:
    start_error = 'Для того чтобы оформить заявку необходимо сперва зарегестрироваться в приложении в качестве клиента '

    request_date = 'Давайте определимся на какую дату  вы хотите сделать заявку.\nВыберити из списка или введити в ' \
                   'формате: 01.01.2024'

    request_date_error = 'Мне нужна дата в формате DD.MM.YYYY или выберити из списка.\nПопробуйте ещё раз'

    request_time = 'Введити время - например так:\n14:30'

    request_time_error = 'Не подходит формат введённых данных. Попробуйте ещё раз'

    request_object_choice = 'Выберите объект'

    request_object_name = 'Пришлите мне название объекта'

    request_object_location = ''

    request_object_location_error = ''

    request_product = 'Выберити нужную продукцию'

    request_volume = 'Сколько кубов?'

    request_volume_error = 'Это должно быть число. Попробуйте ввести ещё раз.'

    request_unloading_method = 'Выберити каким способом вы планируете осуществлять разгрузку:'

    request_unloading_method_error = MessageProduct.error1

    request_unloading_speed = 'Средняя скорость разгрузки данным способом на вашем объекте составляет'

    request_unloading_speed_error = 'Это должно быть число. Попробуйте ввести ещё раз.'

    request_pump_sleeve_length = 'Сколько метров нужна длина стрелы у бетононасоса?'

    request_pump_sleeve_length_error = 'Это должно быть число. Попробуйте ввести ещё раз.'

    request_pump_feed_time = 'Пришлите мне требуемое время подачи бетононасоса - напимер 13:30'

    request_pump_feed_time_error = 'Мне нужно время в формате "HH:MM". Попробуйте ещё раз'

    end = 'Отлично. Я оформила  заявку и передала её на согласование вашему менеджеру. Через некоторое время вам' \
          ' придёт уведомление с результатом'


class MessageRedact:
    start = 'Вот номера ваших заявок доступных для редактирования в настоящий момент:\n' \
            'Пожалуйста выберити номер нужной вам заявки из списка.'
    start_error_not_client = 'Эта функция доступна только для пользователей зарегестрированных в приложении как' \
                             '  "клиент"'
    start_error_no_application = 'К сожалению у вас нет заявок доступных для редактирования в данный момент.\n' \
                                 'Редактировать можно заявки уже согласованные менеджером - но по которым вы ' \
                                 'ещё не подтвердили строительную готовность.\n' \
                                 'Если вам нужно редактировать ещё не согласованную заявку - просто удалити её' \
                                 ' и создайте заново.\n' \
                                 'Если вам нужно изменить уже подтверждённую заявку - срочно свяжитесь с диспетчером' \
                                 ' по телефону. (Приготовтесь назвать ему номер заявки)'

    request_appication_error = 'К сожалению у вас нет других заявок доступных для редактирования в данный момент.\n' \
                               'Редактировать можно заявки уже согласованные менеджером - но по которым вы ' \
                               'ещё не подтвердили строительную готовность.\n' \
                               'Если вам нужно редактировать ещё не согласованную заявку - просто удалити её ' \
                               'и создайте заново.\n' \
                               'Если вам нужно изменить уже подтверждённую заявку - срочно свяжитесь с диспетчером' \
                               ' по телефону. (Приготовтесь назвать ему номер заявки)'

    request_action = "Выберити что вы хотите сделать с этой заявкой"

    request_action_error = 'Другие изменения в заявки не доступны. Если вам необходимо изменить другой параметр ' \
                           'придётся удалить эту заявку и создать новую'


class MessageDelete:
    start_error_no_application = 'У вас нет заявок доступных для отмены в данный момент.\n' \
                                 'Удалить можно  только те заявки  по которым вы ' \
                                 'ещё не подтвердили строительную готовность.\n' \
                                 'Если вам нужно отменить уже подтверждённую заявку - срочно свяжитесь с диспетчером' \
                                 ' по телефону. (Приготовтесь назвать ему номер заявки)'

    start = 'Вот номера ваших заявок доступных для отмены:\n' \
            'Пожалуйста выберити номер нужной вам заявки из списка.'

    request_appication_error = 'К сожалению у вас нет других заявок доступных для отмены.\n' \
                               'Отменить можно заявки  по которым вы ' \
                               'ещё не подтвердили строительную готовность.\n' \
                               'Если вам нужно отменить уже подтверждённую заявку - срочно свяжитесь с диспетчером' \
                               ' по телефону. (Приготовтесь назвать ему номер заявки)'


class MessageUploading:
    request_date = 'Давайте определимся на какую дату  вы хотите получить выборку.\nВыберити из списка или введити в ' \
                   'формате: 01.01.2024'


class MessageWork:
    start_error_not_client = 'Эта функция доступна только для пользователей зарегестрированных в приложении как' \
                             '  "диспетчер"'

    start_error_no_application = "Заявок нет"

    request_application = "Выберити номер заявки"

    request_application_error = "Других доступных заявок нету.\n" \
                                "Доступны только подтверждённые, но не исполненные заявки"

    request_driver = "Выберити водителя"

    request_driver_error = "Вы можете выбрать водителя, который включился в приложении и не занят по заявке.\n" \
                           "Пожалуйста попробуйте ещё раз"

    request_volume = "Укажите отгружаемое количество смеси"

    request_volume_error = MessageApplication.request_volume_error

    request_volume_warning = "Внимание. Это превышает максимально заявленный объём"

    request_travel_time = "Введите ориентировочное время прибытия по новигатору. Например 01:15"

    request_travel_time_error = "Мне нужно время в формате 'MM:HH'  Например 01:15\n" \
                                "Пожалуйста повторите попытку"

    approve_error = 'Что ж бывает. Для того чтобы начать заново нажмите\n/work'

    end = 'Когда прибудете на объект пришлите мне команду \n\n/object\n\n'


class MessageGetLocation:
    no_application = "В настоящий момент у вас нет исполняющихся заявок"

    no_drivers = "В настоящий момент миксер к вам ещё не выехал"

    request_driver = "Выберити из списка чьё местоположение вам необходимо запросить"

    request_driver_error = "К сожалению не удалось отправить запрос"

    notice = "Я направила запрос на отпраку местоположения водителю"


class MessageSendLocation:
    push_location = 'Нажмите "Отправить геолокацию"'

    push_location_error = "Не удалось отправить местоположение"

class MessageInPlace:
    start = 'Принято. Как будете готовы выежать с объекта пожалуйста не забудте меня об этом уведомить,' \
            ' нажав на кнопку "освободился"'
    start_error = 'Эта опция доступна только для водителей'

    not_application = 'У вас сейчас нет активных заявок. Если вы действительно прибыли на объект свяжитесь с' \
                      ' диспетчером для выяснения ситуации'

    request_score = "Оцените пожалуйста объект на предмет качества подъездных путей до места выгрузки.\n" \
                    "От нуля до десяти:\n" \
                    "где 0 будет означать отсутствие возможности доехать до места разгрузки\n" \
                    "а 10 - идеальные подъездные пути"

    thanks = "Спасибо. Ваша оценка принята. Желаю удачного следующего рейса!"

async def get_location_from_driver(state: FSMContext):
    user_data = await state.get_data()
    client = user_data['client']
    driver = user_data['driver']
    application = driver.working_by_application
    the_object = application.the_object
    return f'{driver.name},\n' \
           f'{client.name} {client.last_name}\n' \
           f'{client.post} {client.organization}\n' \
           f'ожидает вас на объекте "{the_object.obj_name}" и запрашивает ваше местоположение\n' \
           f'Для того чтобы отправить своё местоположение нажмите:\n\n/Send_location'


async def set_location_from_driver(state: FSMContext):
    user_data = await state.get_data()
    client = user_data['client']
    driver = user_data['driver']
    mixer = driver.mixer
    return f'{client.name},\n' \
           f'{driver.name} {driver.last_name}\n' \
           f'{mixer.car_brand} {mixer.car_number}\n' \
           f'отправил вам своё местоположение:'


async def set_location_from_driver_error(state: FSMContext):
    user_data = await state.get_data()
    client = user_data['client']
    driver = user_data['driver']
    mixer = driver.mixer
    return f'{client.name},\n' \
           f'{driver.name} {driver.last_name}\n' \
           f'{mixer.car_brand} {mixer.car_number}\n' \
           f'пока не может отправить вам своё местоположение'


async def work_message_to_disp_for_approve(state: FSMContext):
    user_data = await state.get_data()
    application = user_data['application']
    driver = user_data['driver']
    volume = user_data['volume']
    time = user_data['time']
    the_object = application.the_object
    mixer = driver.mixer
    product = application.product
    return f"Хорошо. Я всё правильно поняла?\n" \
           f"По заявке №{application.id} отправляется:\n" \
           f"на объект {the_object.obj_name}\n" \
           f"{driver.name} {driver.last_name} на автомобиле:\n" \
           f"{mixer.car_brand}  {mixer.car_number}\n" \
           f'Везёт: {product.abbreviation}\n' \
           f'В кол-ве: {volume}м3\n' \
           f"Ориентировочное время прибытия {time.strftime('%H:%M')}"


async def work_message_to_client_for_departure_mixer(state: FSMContext):
    user_data = await state.get_data()
    application = user_data['application']
    driver = user_data['driver']
    volume = user_data['volume']
    time = user_data['time']
    remainder = user_data['remainder']
    client = application.creator
    the_object = application.the_object
    mixer = driver.mixer
    product = application.product
    return f'{client.name}, к вам на объект:\n"{the_object.obj_name} "' \
           f'выехал АБС:\n{mixer.car_brand}  {mixer.car_number}\n' \
           f'Везёт: {product.abbreviation}\n' \
           f'В кол-ве: {volume}м3\n' \
           f"Ориентировочное время прибытия {time.strftime('%H:%M')}\n" \
           f"Остаток по заявки: {remainder}м3\n" \
           f"Телефон водителя АБС: {driver.phone}\n" \
           f"Для того чтобы запросить местоположение миксера нажмите\n\n" \
           f"/Get_location"


async def work_message_to_driver(state: FSMContext):
    user_data = await state.get_data()
    application = user_data['application']
    volume = user_data['volume']
    time = user_data['time']
    client = application.creator
    the_object = application.the_object
    product = application.product
    return f'Вам загрузили {product.abbreviation}\n' \
           f'В кол-ве: {volume}м3\n' \
           f'Контакт для связи:\n' \
           f'{client.phone}\n' \
           f'{client.post} {client.organization} {client.name} {client.last_name}\n' \
           f'Ориентировочное время прибытия {time.strftime("%H:%M")}\n' \
           f'На объект: "{the_object.obj_name}"'


def approve_answer_to_disp(remainder):
    return f"Отлично. Я внесу необходимые изменения в БД и отправлю уведомления заказчику.\nОстаток по заявке " \
           f"составляет {remainder}м3"


def do_end(application):
    return f'Отлично. Я зарегестрировала вашу заявку за номером №{application.id} и передала её на согласование' \
           f' вашему менеджеру. Через некоторое время вам придёт уведомление с результатом'


def do_answer_about_approve(client, application):
    return f"{client.name}, информирую вас о том, что ваша заявка  №{application.id} согласована и передана в работу" \
           f" на завод\n. За 2 часа до прибытия вам поступит сообщение с возможностью подтвердить готовность " \
           f"на объекте.\n" \
           f"В случае изменения ситуации необходимо заблоговременно проинформировать завод. Это можно сделать через" \
           f" приложение - нажав команду 'редактировать заявку'."


def do_rejection_about_approve(client, application, text):
    return f'Сожалею {client.name}. Ваша заявка №{application.id} отклонена по причине:\n"{text}"'
