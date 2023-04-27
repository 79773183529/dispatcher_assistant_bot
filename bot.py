from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os
from dotenv import load_dotenv, find_dotenv

from apscheduler.schedulers.asyncio import AsyncIOScheduler


load_dotenv(find_dotenv())
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
bot.parse_mode = 'HTML'
dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()

id_creator = 1068817703
id_Roman = 5447383130

id_group_list = [id_creator, id_Roman]
