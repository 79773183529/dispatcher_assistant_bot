import asyncio

import emoji
from aiogram.types import BotCommand

from application import register_handlers_application
from aiogram import executor, Bot

from bot import bot, dp, scheduler
from common import register_handlers_common
from registration import register_handlers_registration
from reminders import schedule_jobs
from sendLocation import register_handlers_location
from reminders import register_handlers_reminders
from redact import register_handlers_redact
from delete import register_handlers_delete
from uploading import register_handlers_uploading
from work import register_handlers_work
from driver_on import register_handlers_driver_on
from get_location import register_handlers_get_location
from send_location import register_handlers_send_location
from in_place import register_handlers_send_in_place


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/registration", description=f"{emoji.emojize(':magnifying_glass_tilted_left:')} "
                                                        f"Регистрация"),

        BotCommand(command="/application", description=f"{emoji.emojize(':magnifying_glass_tilted_left:')} "
                                                       f"Оформить заявку"),

        BotCommand(command="/redact", description=f"{emoji.emojize(':magnifying_glass_tilted_left:')} "
                                                  f"Редактировать  заявку"),

        BotCommand(command="/delete", description=f"{emoji.emojize(':wastebasket:')} Отменить заявку\n\n"),

        BotCommand(command="/uploading", description=f"{emoji.emojize(':chequered_flag:')} Выгрузить заявки"),

        BotCommand(command="/cancel", description=f"{emoji.emojize(':chequered_flag:')} Выход"),
    ]
    await bot.set_my_commands(commands)


async def on_startup(dp):
    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_location(dp)
    register_handlers_registration(dp)
    register_handlers_application(dp)
    register_handlers_reminders(dp)
    register_handlers_redact(dp)
    register_handlers_delete(dp)
    register_handlers_uploading(dp)
    register_handlers_work(dp)
    register_handlers_driver_on(dp)
    register_handlers_get_location(dp)
    register_handlers_send_location(dp)
    register_handlers_send_in_place(dp)

    await set_commands(bot)  # Установка команд бота

    await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)

    # запуск планировщика
    scheduler.start()
    schedule_jobs()

    for alpha in "DispatcherAssistantBoT:  OnLine":
        print(alpha, end='')
        await asyncio.sleep(0.3)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
