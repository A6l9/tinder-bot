from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config.config import BOT_TOKEN
from database.database import DATABASE_URL
from database.controller import BaseInterface
from misc.temp_storage import UserManager


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
db = BaseInterface(DATABASE_URL)
dp = Dispatcher(storage=MemoryStorage())
user_manager = UserManager()
