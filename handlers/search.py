from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db.database import get_products, search_products

router = Router()

class Search(StatesGroup):
    waiting_for_query = State()

@router.callback_query(F.data == "view_products")
async def view_products_callback(callback: CallbackQuery):
    products = get_products()
    if products:
        response = "Mavjud mahsulotlar:\n"
        for product in products:
            response += f"ID: {product[0]}\nNomi: {product[1]}\nNarxi: {product[2]}\nTavsifi: {product[3]}\nKategoriyasi: {product[4]}\n\n"
        await callback.message.answer(response)
    else:
        await callback.message.answer("Hozircha mahsulotlar mavjud emas.")
    await callback.answer()

@router.callback_query(F.data == "search_product")
async def search_product_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Qidirish uchun mahsulot nomini kiriting:")
    await state.set_state(Search.waiting_for_query)
    await callback.answer()

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