from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from message_text import ButtonRegistration


# Создаёт клавиатуру с кнопками отправить контакт
def make_keyboard_contact():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(ButtonRegistration.request_contact, request_contact=True))
    return keyboard


# Создаёт клавиатуру с кнопками отправить геолокацию
def make_keyboard_location():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(ButtonRegistration.request_location, request_location=True))
    keyboard.add(KeyboardButton(ButtonRegistration.send_later))
    return keyboard


# Создаёт клавиатуру с кнопкой отправить позже
def make_keyboard_send_later():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(ButtonRegistration.send_later))
    return keyboard


# Создаёт клавиатуру с ролями для приложения
def make_keyboard_roles():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(ButtonRegistration.role0))
    keyboard.add(KeyboardButton(ButtonRegistration.role1))
    keyboard.add(KeyboardButton(ButtonRegistration.role2))
    keyboard.add(KeyboardButton(ButtonRegistration.role3))
    return keyboard


# Создаёт клавиатуру с кнопками из полученного списка
def make_keyboard_by_list(button_list, key_other="Другое"):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for el in button_list:
        keyboard.add(KeyboardButton(el))
    keyboard.add(KeyboardButton(key_other))
    return keyboard


# Создаёт клавиатуру с кнопками из полученного списка
def make_keyboard_by_list_only(button_list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for el in button_list:
        keyboard.add(KeyboardButton(el))
    return keyboard


# Создаёт клавиатуру для утверждения регистрации
def make_keyboard_approval_registration():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Утвердить'))
    keyboard.add(KeyboardButton('Отклонить'))
    return keyboard


# Создаёт клавиатуру для согласования
def make_keyboard_approval():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Согласовать'))
    return keyboard
