from aiogram.fsm.state import StatesGroup, State

class Get_posts(StatesGroup):
    receive = State()

class Creating(StatesGroup):
    word_writing = State()
    definition_writing = State()
    description_writing = State()