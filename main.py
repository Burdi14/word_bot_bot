import logging
from aiogram.utils.chat_action import ChatActionMiddleware
from handlers import router, send_word, post_data
import asyncio
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery
from load_dotenv import load_dotenv
from aiogram.filters import Command
from kb import you_sure_post_markup
from bot import bot, dp
import db_scripts
from aiogram import F
load_dotenv()


@dp.message(Command('post_word'))
async def post_word(msg: Message):
    msg.anwer('отправить слово дня?', reply_markup=you_sure_post_markup)


@dp.callback_query(F.data == 'post')
async def post(call: CallbackQuery):
    users_to_send = db_scripts.get_active_users()
    if db_scripts.find_word(post_data['word']) is None:
        db_scripts.insert_word(post_data['word'], post_data['definition'], post_data['description'], is_sent='true')
    else:
        db_scripts.update_word(post_data['word'], post_data['definition'], post_data['description'], is_sent='true')
    text = send_word()
    for user_id in users_to_send:
        await bot.send_message(user_id[0], text)

async def main():
    dp.include_router(router)
    dp.message.middleware(ChatActionMiddleware())
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
