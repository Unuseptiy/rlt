import asyncio
import sys
import logging
from dotenv import dotenv_values

from aiogram.enums import ParseMode
from aiogram import Bot

from bot import dp


async def main() -> None:
    TOKEN = dotenv_values(".env")["BOT_TOKEN"]
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
