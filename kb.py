from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

admin_menu = [
  [InlineKeyboardButton(text = 'новое слово', callback_data = 'admin_new_word')]
    [InlineKeyboardButton(text = 'добавить админа', callback_data = 'add_admin')]
]

admin_menu = InlineKeyboardMarkup(inline_keyboard=
                                  admin_menu)
new_word_menu =[
    [InlineKeyboardButton(text = 'слово', callback_data = 'get_word'),
     InlineKeyboardButton(text = 'определение', callback_data = 'get_definition'),
     InlineKeyboardButton(text = 'пояснение', callback_data = 'get_description')],
  [ InlineKeyboardButton(text = 'посмотреть', callback_data = 'get_look'),
     InlineKeyboardButton(text = 'отправить', callback_data = 'send_word'),
    InlineKeyboardButton(text = 'отменить', callback_data = 'back_to_menu'),]
]

new_word_menu_markup = InlineKeyboardMarkup(inline_keyboard=new_word_menu)