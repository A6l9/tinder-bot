from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from utils.config import BOT_TOKEN
from database.database import DATABASE_URL
from database.controller import BaseInterface


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
db = BaseInterface(DATABASE_URL)
dp = Dispatcher(storage=MemoryStorage())