from aiogram.types import BotCommand, BotCommandScopeDefault
from loader import bot


async def set_commands():
    """
    Функция для создания набора команд бота
    :return:
    """
    commands = [BotCommand(command='start', description='Начать поиск'),
                ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
