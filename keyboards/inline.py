from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Kategoriya qo'shish", callback_data='add_category'),
         InlineKeyboardButton(text="Mahsulot qo'shish", callback_data='add_product')],
        [InlineKeyboardButton(text="Mahsulotlarni ko'rish", callback_data='view_products'),
         InlineKeyboardButton(text="Mahsulot qidirish", callback_data='search_product')],
        [InlineKeyboardButton(text="Kategoriyani o'chirish", callback_data='delete_category'),
         InlineKeyboardButton(text="Mahsulotni o'chirish", callback_data='delete_product')],
        [InlineKeyboardButton(text="Kategoriyani o'zgartirish", callback_data='edit_category'),
         InlineKeyboardButton(text="Mahsulotni o'zgartirish", callback_data='edit_product')]
    ])
    return keyboard

def get_categories_keyboard(categories, prefix: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=cat[1], callback_data=f"{prefix}_{cat[0]}")] for cat in categories
    ])
    return keyboard

def get_products_keyboard(products, prefix: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=prod[1], callback_data=f"{prefix}_{prod[0]}")] for prod in products
    ])
    return keyboard