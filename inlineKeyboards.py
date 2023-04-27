from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
import datetime


def dynamic_keyboard(number=0):
    markup = types.InlineKeyboardMarkup()
    # создаем кнопки
    button_up = InlineKeyboardButton(text=f'Увеличить', callback_data="up")
    button_down = InlineKeyboardButton(text=f'Уменьшить', callback_data="down")
    button_send = InlineKeyboardButton(text=f'Подтвердить: {number} кубов/час', callback_data="send")
    markup.row(button_down, button_up)
    markup.row(button_send)
    return markup


# Динамическая клавиатура для корректировки времени подачи по заявке
def dynamic_time(time: datetime):
    markup = types.InlineKeyboardMarkup()
    # создаем кнопки
    button_up = InlineKeyboardButton(text=f'Увеличить на 30мин', callback_data="forward")
    button_down = InlineKeyboardButton(text=f'Уменьшить на 30мин', callback_data="back")
    button_send = InlineKeyboardButton(text=f'Подтвердить на {time.strftime("%H:%M")}',
                                       callback_data="now")
    markup.row(button_down, button_up)
    markup.row(button_send)
    return markup


# Динамическая клавиатура для корректировки объёма по заявке
def dynamic_volume(volume=0):
    markup = types.InlineKeyboardMarkup()
    # создаем кнопки
    button_up = InlineKeyboardButton(text=f'Добавить 0,5 куба', callback_data="up")
    button_down = InlineKeyboardButton(text=f'Отнять 0,5 куба', callback_data="down")
    button_send = InlineKeyboardButton(text=f'Подтвердить: {volume} м3', callback_data="send")
    markup.row(button_down, button_up)
    markup.row(button_send)
    return markup


# Динамическая клавиатура для корректировки объёма по заявке
def dynamic_score(score=7):
    markup = types.InlineKeyboardMarkup()
    # создаем кнопки
    button_up = InlineKeyboardButton(text=f'Добавить 1 бал', callback_data="up")
    button_down = InlineKeyboardButton(text=f'Отнять 1 бал', callback_data="down")
    button_send = InlineKeyboardButton(text=f'Поставить {score} бал(ов)', callback_data="send")
    markup.row(button_down, button_up)
    markup.row(button_send)
    return markup
