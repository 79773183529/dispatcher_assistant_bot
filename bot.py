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

id_creator = os.getenv('id_creator')
id_Roman = os.getenv('id_Roman')

id_group_list = [id_creator, id_Roman]

YA_TOKEN = os.getenv('YA_TOKEN')
