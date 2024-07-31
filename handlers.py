from aiogram import Router, types, F, flags
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text, Bold, Italic
from states import Get_posts, Creating
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER
import kb
import text
import db_scripts


router = Router()
users_received_count = 0
post_data = {
    'word': '',
    'definition': '',
    'description': ''
}
user_id_to_send = []


def wrap_post(word, definition, description):
    msg = Text(Bold('слово дня'), '\n\n', Italic(post_data['word']), ' - ',
               post_data['definition'], '\n\n[', post_data['description'], ']\n#словодня', )
    return msg


def send_word(post_data):
    msg = wrap_post(post_data['word'], post_data['definition'], post_data['description'])
    post_data['word'] = ''
    post_data['definition'] = ''
    post_data['description'] = ''
    return msg


@router.message(Command('start'))
async def start_handler(msg: Message, state: FSMContext):
    if db_scripts.find_admin(str(msg.from_user.id)):
        await msg.answer('имеются для меня таски?', reply_markup=kb.admin_menu)
    else:
        user_id_to_send.append(msg.from_user.id)
        await msg.answer(text='теперь ты будешь получать слово дня!')
        await state.set_state(Get_posts.receive)


@router.callback_query(F.data == 'admin_new_word')
async def create_new_post(callback: CallbackQuery):
    await callback.message.answer(text='enter new word boss', reply_markup=kb.new_word_menu_markup)


@router.callback_query(F.data == 'get_word')
async def set_get_word_state(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Creating.word_writing)


@router.callback_query(F.data == 'get_definition')
async def set_get_definition_state(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Creating.definition_writing)


@router.callback_query(F.data == 'get_description')
async def set_get_description_state(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Creating.description_writing)


@router.message(Creating.word_writing)
async def get_word(msg: Message, state: FSMContext):
    word = msg.text
    post_data['word'] = word
    await msg.answer('word''s received')
    await state.clear()


@router.message(Creating.definition_writing)
async def get_definition(msg: Message, state: FSMContext):
    definition = msg.text
    post_data['definition'] = definition
    await msg.answer('done')
    await state.clear()


@router.message(Creating.description_writing)
async def get_description(msg: Message, state: FSMContext):
    description = msg.text
    post_data['description'] = description
    await msg.answer('done')
    await state.clear()


@router.message(Command('get_look'))
async def get_look(msg: Message, state: FSMContext):
    await msg.answer(post_data['word'] + '\n' + post_data['definition'] + '\n' + post_data['description'])


# @router.callback_query(F.data == 'send_word')
# async def send_word(callback: CallbackQuery,state: FSMContext):
#     for user in user_id_to_send:


@router.callback_query()
async def add_user(callback: CallbackQuery):
    print()


@router.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def on_user_leave(event: ChatMemberUpdated):
    user_id_to_send.remove(event.from_user.id)


@router.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: ChatMemberUpdated):
    user_id_to_send.append(event.from_user.id)
    await event.answer('теперь ты будешь получать слово дня!')


