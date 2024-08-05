import logging
import os
from aiogram.enums import ParseMode
from aiogram.utils.chat_action import ChatActionMiddleware
from handlers import router,wrap_post,  send_word, post_data
import asyncio
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery
from load_dotenv import load_dotenv
from aiogram.filters import Command
import kb
from bot import bot, dp
from text import menu_text
import db_scripts
from aiogram import F
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from schedule_mailing import daily_mailing

load_dotenv()

async def start_mailing():
    users_to_send = db_scripts.get_active_users()
    if db_scripts.find_word(post_data['word']) is None:
        db_scripts.insert_word(post_data['word'], post_data['definition'], post_data['description'], is_sent='true')
    else:
        db_scripts.update_word(post_data['word'], post_data['definition'], post_data['description'], is_sent='true')
    text = send_word()
    for user_id in users_to_send:
        await bot.send_message(user_id[0], text)

@dp.message(Command('post_word'))
async def post_word(msg: Message):
    await msg.answer(wrap_post(post_data['word'], post_data['definition'], post_data['description']))
    await msg.answer('отправить слово дня?', reply_markup=kb.you_sure_post_markup)


@dp.callback_query(F.data == 'post')
async def post(callback: CallbackQuery):
    await start_mailing()
    if str(os.getenv('MAIN_ADMIN_ID')) == str(callback.from_user.id):
        await callback.message.answer(text=menu_text, reply_markup=kb.main_admin_menu_markup)
    else:
        await callback.message.answer(text=menu_text, reply_markup=kb.admin_menu_markup)

def set_scheduled_jobs(scheduler):
    scheduler.add_job(daily_mailing, "cron", hour=14, minute=14)

async def main():
    dp.include_router(router)
    dp.message.middleware(ChatActionMiddleware())

    scheduler = AsyncIOScheduler()
    set_scheduled_jobs(scheduler)
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
