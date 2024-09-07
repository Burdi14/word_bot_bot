from bot import bot
import db_scripts
import os
from handlers import wrap_post
from aiogram.enums import ParseMode
import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

async def daily_mailing():
    if os.getenv('next_word') == '':
        unused_words = db_scripts.get_unused_words()
        if unused_words is None:
            await bot.send_message(os.getenv('MAIN_ADMIN_ID'), 'админ, сегодня нет слов для ежедневной рассылки')
        else:
            word_data = db_scripts.find_word(unused_words[-1])
            users_to_send = db_scripts.get_active_users()
            db_scripts.update_word(word_data[0], word_data[1], word_data[2], is_sent='true')
            for user_id in users_to_send:
                await bot.send_message(user_id[0], text=wrap_post(word_data[0], word_data[1], word_data[2]), parse_mode=ParseMode.HTML)
    else:
        word = os.getenv('next_word')
        word_data = db_scripts.find_word(word)
        users_to_send = db_scripts.get_active_users()
        db_scripts.update_word(word_data[0], word_data[1], word_data[2], is_sent='true')
        for user_id in users_to_send:
            print(user_id[0])
            await bot.send_message(user_id[0], text=wrap_post(word_data[0], word_data[1], word_data[2]),parse_mode=ParseMode.HTML)
        dotenv.set_key(dotenv_file, 'next_word', '')
        os.environ['next_word'] = ''
