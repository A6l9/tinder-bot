from aiogram.types import BotCommand, BotCommandScopeDefault
from loader import bot


async def set_commands():
    """
    Функция для создания набора команд бота
    :return:
    """
    commands = [BotCommand(command='start', description='Начать поиск'),
                BotCommand(command='show_my_profile', description='Показать мой профиль'),
                BotCommand(command='change_search_parameters', description='Изменить параметры поиска')
                ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
