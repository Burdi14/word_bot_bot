from aiogram.fsm.state import StatesGroup, State

class Word_setting(StatesGroup):
    word_writing = State()
    definition_writing = State()
    description_writing = State()
    check_word = State()
    writing_word_for_choosing = State()
    writing_to_delete = State()

class Admin_setting(StatesGroup):
    add_admin = State()
    delete_admin = State()