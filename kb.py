from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
main_admin_menu = [
  [InlineKeyboardButton(text = 'новое слово', callback_data = 'admin_new_word')],
    [InlineKeyboardButton(text='посмотреть неиспользованные', callback_data='get_unused_words')],
    [InlineKeyboardButton(text = 'добавить админа', callback_data = 'add_admin'),
     InlineKeyboardButton(text = 'удалить админа', callback_data = 'delete_admin')]
]

admin_menu = [
  [InlineKeyboardButton(text='новое слово', callback_data = 'admin_new_word')],
[InlineKeyboardButton(text='посмотреть неиспользованные', callback_data='get_unused_words')]

]
new_word_menu =[
    [InlineKeyboardButton(text = 'слово', callback_data = 'get_word'),
     InlineKeyboardButton(text = 'определение', callback_data = 'get_definition'),
     InlineKeyboardButton(text = 'пояснение', callback_data = 'get_description')],
  [InlineKeyboardButton(text = 'посмотреть', callback_data = 'get_look'),
   InlineKeyboardButton(text = 'сбросить', callback_data = 'reset'),
   InlineKeyboardButton(text='добавить в список', callback_data = 'add_to_list')],
[InlineKeyboardButton(text='меню', callback_data = 'back_to_menu')]
]

old_word_menu = [
    [InlineKeyboardButton(text='посмотреть слово', callback_data='look_unused_word')],
    [InlineKeyboardButton(text='удалить слово', callback_data='delete_unused_word')],
    [InlineKeyboardButton(text='выбрать слово', callback_data='choose_unused_word')],
    [InlineKeyboardButton(text='меню', callback_data = 'back_to_menu')]
]

you_sure_menu = [
    [InlineKeyboardButton(text='✅да', callback_data = 'add_word_to_db')],
    [InlineKeyboardButton(text='❌нет', callback_data = 'admin_new_word')]
]
you_sure_post = [
    [InlineKeyboardButton(text='✅да', callback_data = 'post')],
    [InlineKeyboardButton(text='❌нет', callback_data = 'admin_new_word')]
]

you_sure_post_markup = InlineKeyboardMarkup(inline_keyboard=you_sure_post)
you_sure_menu_markup = InlineKeyboardMarkup(inline_keyboard=you_sure_menu)
new_word_menu_markup = InlineKeyboardMarkup(inline_keyboard=new_word_menu, resize_keyboard=False)
main_admin_menu_markup = InlineKeyboardMarkup(inline_keyboard=main_admin_menu)
admin_menu_markup = InlineKeyboardMarkup(inline_keyboard=admin_menu)
old_word_menu_markup = InlineKeyboardMarkup(inline_keyboard=old_word_menu)

