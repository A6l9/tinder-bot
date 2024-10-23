
from loader import dp, bot
from handlers.default.start import start_router
from handlers.custom.filling_out_a_profile import profile_router
from handlers.custom.show_questionnaire import show_router
from handlers.custom.edit_profile import edit_profile_router
from handlers.custom.pagination_handler import pagination_router
from utils.set_commands import set_commands
import asyncio
from loguru import logger


async def main():

    logger.info('The bot start working')
    dp.include_routers(start_router, profile_router, show_router, edit_profile_router, pagination_router)
    await dp.start_polling(bot)
    await set_commands()


if __name__ == "__main__":
    asyncio.run(main())
