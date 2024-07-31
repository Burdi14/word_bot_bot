import logging
from aiogram import Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware
from handlers import router
import asyncio
from aiogram.types import Message
from aiogram import Bot
from load_dotenv import load_dotenv
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.bot import DefaultBotProperties
import os

load_dotenv()

async def main():
    TOKEN = os.getenv('TOKEN')
    print(TOKEN)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    dp.message.middleware(ChatActionMiddleware())
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
