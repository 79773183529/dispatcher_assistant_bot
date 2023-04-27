import asyncio
import logging

import emoji
from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.utils import executor

from common import register_handlers_common
from sendLocation import register_handlers_location
from registration import register_handlers_registration
from application import register_handlers_application
from test import register_handlers_test

from reminders import schedule_jobs

from bot import bot, dp, scheduler

logging.basicConfig(level=logging.INFO)


async def main():

    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_location(dp)
    register_handlers_registration(dp)
    register_handlers_application(dp)
    register_handlers_test(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)

    await dp.start_polling()
    schedule_jobs()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/registration", description=f"{emoji.emojize(':magnifying_glass_tilted_left:')} "
                                                            f"Регистрация"),

        BotCommand(command="/application", description=f"{emoji.emojize(':magnifying_glass_tilted_left:')} "
                                                        f"Оформить заявку"),
        BotCommand(command="/cancel", description=f"{emoji.emojize(':chequered_flag:')} Выход"),
    ]
    await bot.set_my_commands(commands)


if __name__ == '__main__':
    scheduler.start()
    asyncio.run(main())
    # executor.start_polling(dp, on_startup=on_startup, skip_updates=False)


