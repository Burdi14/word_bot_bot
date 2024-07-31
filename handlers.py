import os

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import text
from states import Word_setting, Admin_setting
import kb
import db_scripts
from text import menu_text, greet
from load_dotenv import load_dotenv
load_dotenv()

router = Router()

post_data = {
    'word': '',
    'definition': '',
    'description': ''
}

def wrap_post(word, definition, description):
    msg = f'<b>слово дня</b>\n\n<i>{word}</i> - {definition}\n\n[{description}]\n#словодня'
    return msg

def send_word():
    global post_data
    msg = wrap_post(post_data['word'], post_data['definition'], post_data['description'])
    post_data['word'] = ''
    post_data['definition'] = ''
    post_data['description'] = ''
    return msg

@router.message(Command('start'))
async def start_handler(msg: Message, state: FSMContext):
    if str(msg.from_user.id) == os.getenv('MAIN_ADMIN_ID'):
        await msg.answer(menu_text, reply_markup=kb.main_admin_menu_markup)
    elif db_scripts.find_admin(str(msg.from_user.id)):
        await msg.answer(menu_text, reply_markup=kb.admin_menu_markup)
    else:
        db_scripts.insert_new_user(str(msg.from_user.id), str(msg.from_user.username))
        await msg.answer(text=greet.format(name=msg.from_user.first_name))


@router.callback_query(F.data == 'admin_new_word')
async def create_new_post(callback: CallbackQuery):
    await callback.message.answer(text='enter new word', reply_markup=kb.new_word_menu_markup)


@router.callback_query(F.data == 'get_word')
async def set_get_word_state(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Word_setting.word_writing)
    await callback.message.answer('введите слово')


@router.callback_query(F.data == 'get_definition')
async def set_get_definition_state(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Word_setting.definition_writing)
    await callback.message.answer('введите определение')


@router.callback_query(F.data == 'get_description')
async def set_get_description_state(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Word_setting.description_writing)
    await callback.message.answer('введите описание')


@router.message(Word_setting.word_writing)
async def get_word(msg: Message, state: FSMContext):
    word = msg.text
    global post_data
    post_data['word'] = word
    await msg.answer("word's received", reply_markup=kb.new_word_menu_markup)
    await state.clear()


@router.message(Word_setting.definition_writing)
async def get_definition(msg: Message, state: FSMContext):
    definition = msg.text
    global post_data
    post_data['definition'] = definition
    await msg.answer("definition's received", reply_markup=kb.new_word_menu_markup)
    await state.clear()


@router.message(Word_setting.description_writing)
async def get_description(msg: Message, state: FSMContext):
    description = msg.text
    global post_data
    post_data['description'] = description
    await msg.answer("description's received", reply_markup=kb.new_word_menu_markup)
    await state.clear()

@router.callback_query(F.data == 'get_look')
async def get_look(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=wrap_post(post_data['word'], post_data['definition'], post_data['description']), parse_mode=ParseMode.HTML)

@router.callback_query(F.data == 'get_unused_words')
async def get_unused_words_handler(callback: CallbackQuery):
    list_words = db_scripts.get_unused_words()
    list_words = [str(x)[2:-3]+'\n' for x in list_words]
    res = ''.join(sorted(list_words))
    if res == []:
        await callback.message.answer(text='no unused words')
    else:
        await callback.message.answer(text=res, reply_markup=kb.old_word_menu_markup)

@router.callback_query(F.data == 'look_unused_word')
async def set_get_unused_word_state(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Word_setting.check_word)
    text = callback.message.text
    await callback.message.edit_text(text)
    await callback.message.answer(text='введите слово для получения информации')

@router.message(Word_setting.check_word)
async def write_word_to_check(msg: Message, state: FSMContext):
    word_data = db_scripts.find_word(msg.text)
    print(word_data)
    await state.clear()
    try:
        await msg.answer(text=wrap_post(word_data[0], word_data[1], word_data[2]), parse_mode=ParseMode.HTML, reply_markup=kb.old_word_menu_markup)
    except:
        await msg.answer(text='the word is not found', reply_markup=kb.old_word_menu_markup)


@router.callback_query(F.data == 'back_to_menu')
async def back_to_menu(callback: CallbackQuery):
    user_id = callback.message.from_user.id
    if user_id == os.getenv('MAIN_ADMIN_ID'):
        await callback.message.edit_text(text=menu_text, reply_markup=kb.main_admin_menu_markup)
    else:
        await callback.message.edit_text(text=menu_text, reply_markup=kb.admin_menu_markup)

@router.callback_query(F.data == 'add_admin')
async def add_admin_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Admin_setting.add_admin)
    await callback.message.edit_text('введите username нового админа')

@router.message(Admin_setting.add_admin)
async def writing_new_admin_handler(msg: Message, state: FSMContext):
    id = db_scripts.find_id_by_username(str(msg.text))
    db_scripts.insert_new_addmin(str(id)[1:-2])
    await state.clear()
    await msg.answer('есть таски?', reply_markup=kb.main_admin_menu_markup)


@router.callback_query(F.data == 'delete_admin')
async def delete_admin_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Admin_setting.delete_admin)
    await callback.message.edit_text('введите username админа')


@router.message(Admin_setting.delete_admin)
async def writing_deleting_admin_handler(msg: Message, state: FSMContext):
    id = db_scripts.find_id_by_username(str(msg.text))
    db_scripts.delete_admin(str(id)[1:-2])
    await state.clear()
    await msg.answer('есть таски?', reply_markup=kb.main_admin_menu_markup)

@router.callback_query(F.data == 'add_to_list')
async def add_to_list_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text=wrap_post(post_data['word'], post_data['definition'], post_data['description']))
    await callback.message.edit_text(text='добавить слово в список?', reply_markup=kb.you_sure_menu_markup)

@router.callback_query(F.data == 'add_word_to_db')
async def add_word_to_db_handler(callback: CallbackQuery, state: FSMContext):
    if db_scripts.find_word(callback.message.text) is None:
        db_scripts.insert_word(post_data['word'], post_data['definition'], post_data['description'], is_sent='false')
    else:
        db_scripts.update_word(post_data['word'], post_data['definition'], post_data['description'], is_sent='false')
    await callback.message.edit_text(text='слово добавлено.\nесть еще таски?', reply_markup=kb.admin_menu_markup)

@router.callback_query(F.data == 'choose_unused_word')
async def choose_unused_word_handler(callback: CallbackQuery, state: FSMContext):
    text = callback.message.text
    await callback.message.edit_text(text)
    await callback.message.answer('напишите слово для cохранения в буфер')
    await state.set_state(Word_setting.writing_word_for_choosing)

@router.message(Word_setting.writing_word_for_choosing)
async def writing_word_for_choosing_handler(msg: Message, state: FSMContext):
    global post_data
    word_data = db_scripts.find_word(msg.text)
    if word_data:
        print(word_data[0])
        post_data['word'] = word_data[0]
        post_data['definition'] = word_data[1]
        post_data['description'] = word_data[2]
        await msg.answer(text='ваше слово дня', reply_markup=kb.new_word_menu_markup)
    else:
        await msg.answer(text='input error', reply_markup=kb.old_word_menu_markup)
    await state.clear()

@router.callback_query(F.data == 'delete_unused_word')
async def delete_unused_word_handler(callback: CallbackQuery, state: FSMContext):
    text = callback.message.text
    await callback.message.edit_text(text)
    await callback.message.answer('напищите слово для удаления')
    await state.set_state(Word_setting.writing_to_delete)

@router.message(Word_setting.writing_to_delete)
async def writing_to_delete_handler(msg: Message, state: FSMContext):
    text = msg.text
    try:
        db_scripts.delete_word(text)
        await msg.answer(text='слово удалено', reply_markup=kb.old_word_menu_markup)
    except:
        await msg.answer(text='input error', reply_markup=kb.old_word_menu_markup)
    await state.clear()