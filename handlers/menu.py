from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db.database import get_user, get_categories, get_products, search_products
from keyboards.inline import get_main_menu, get_categories_keyboard, get_products_keyboard

router = Router()

class Search(StatesGroup):
    waiting_for_query = State()

@router.message(Command("menu"))
async def menu_command(message: Message):
    await message.answer("Boshqaruv paneli:", reply_markup=get_main_menu())

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "/start - Ro'yxatdan o'tish yoki menyuni qayta ko'rsatish\n"
        "/categories - Kategoriyalarni ko'rish\n"
        "/products - Mahsulotlar ro'yxati\n"
        "/add_category - Yangi kategoriya qo'shish\n"
        "/add_product - Yangi mahsulot qo'shish\n"
        "/search - Mahsulot qidirish"
    )

@router.message(Command("categories"))
async def cmd_categories(message: Message):
    if not get_user(message.from_user.id):
        return await message.reply("❌ Ro‘yxatdan o‘tmagansiz.")
    cats = get_categories()
    if cats:
        await message.answer("📂 Kategoriyalar:", reply_markup=get_categories_keyboard(cats, "view_cat"))
    else:
        await message.answer("Hozircha kategoriyalar mavjud emas.")

@router.message(Command("products"))
async def cmd_products(message: Message):
    if not get_user(message.from_user.id):
        return await message.reply("❌ Ro‘yxatdan o‘tmagansiz.")
    prods = get_products()
    if prods:
        await message.answer("📦 Mahsulotlar:", reply_markup=get_products_keyboard(prods, "view_prod"))
    else:
        await message.answer("Hozircha mahsulotlar mavjud emas.")

@router.message(Command("search"))
async def cmd_search(message: Message, state: FSMContext):
    if not get_user(message.from_user.id):
        return await message.reply("❌ Ro‘yxatdan o‘tmagansiz.")
    await message.answer("Mahsulot nomini kiriting:")
    await state.set_state(Search.waiting_for_query)

@router.message(Search.waiting_for_query)
async def process_search(message: Message, state: FSMContext):
    products = search_products(message.text)
    if products:
        response = "Qidiruv natijalari:\n"
        for product in products:
            response += f"ID: {product[0]}\nNomi: {product[1]}\nNarxi: {product[2]}\nTavsifi: {product[3]}\nKategoriyasi: {product[4]}\n\n"
        await message.answer(response)
    else:
        await message.answer("Hech qanday mahsulot topilmadi.")
    await state.clear()