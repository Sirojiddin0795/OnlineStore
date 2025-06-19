from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from db.database import get_categories, add_product, get_products, delete_product, get_product, update_product
from keyboards.inline import get_categories_keyboard, get_products_keyboard

router = Router()

class Product(StatesGroup):
    waiting_for_category = State()
    waiting_for_name = State()
    waiting_for_price = State()
    waiting_for_description = State()
    waiting_for_new_name = State()
    waiting_for_new_category = State()
    waiting_for_new_price = State()
    waiting_for_new_description = State()

@router.message(Command("add_product"))
async def add_product_command(message: Message, state: FSMContext):
    if not get_user(message.from_user.id):
        return await message.reply("❌ Ro‘yxatdan o‘tmagansiz.")
    categories = get_categories()
    if categories:
        await message.answer("Mahsulot qo'shish uchun kategoriyani tanlang:",
                             reply_markup=get_categories_keyboard(categories, "cat"))
        await state.set_state(Product.waiting_for_category)
    else:
        await message.answer("Hozircha kategoriyalar mavjud emas. Avval kategoriya qo'shing.")

@router.callback_query(F.data == "add_product")
async def add_product_callback(callback: CallbackQuery, state: FSMContext):
    categories = get_categories()
    if categories:
        await callback.message.answer("Mahsulot qo'shish uchun kategoriyani tanlang:",
                                     reply_markup=get_categories_keyboard(categories, "cat"))
        await state.set_state(Product.waiting_for_category)
    else:
        await callback.message.answer("Hozircha kategoriyalar mavjud emas. Avval kategoriya qo'shing.")
    await callback.answer()

@router.callback_query(F.data.startswith("cat_"))
async def process_category_selection(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split("_")[1])
    await state.update_data(category_id=category_id)
    await callback.message.answer("Mahsulot nomini kiriting:")
    await state.set_state(Product.waiting_for_name)
    await callback.answer()

@router.message(Product.waiting_for_name)
async def process_product_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Mahsulot narxini kiriting:")
    await state.set_state(Product.waiting_for_price)

@router.message(Product.waiting_for_price)
async def process_product_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(price=price)
        await message.answer("Mahsulot tavsifini kiriting:")
        await state.set_state(Product.waiting_for_description)
    except ValueError:
        await message.answer("Iltimos, to'g'ri narx kiriting (masalan, 100.50):")

@router.message(Product.waiting_for_description)
async def process_product_description(message: Message, state: FSMContext):
    user_data = await state.get_data()
    add_product(user_data['name'], user_data['category_id'], user_data['price'], message.text)
    await message.answer(f"Mahsulot '{user_data['name']}' qo'shildi!")
    await state.clear()

@router.callback_query(F.data == "delete_product")
async def delete_product_callback(callback: CallbackQuery):
    products = get_products()
    if products:
        await callback.message.answer("O'chirish uchun mahsulotni tanlang:",
                                     reply_markup=get_products_keyboard(products, "del_prod"))
    else:
        await callback.message.answer("Hozircha mahsulotlar mavjud emas.")
    await callback.answer()

@router.callback_query(F.data.startswith("del_prod_"))
async def process_delete_product(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[2])
    delete_product(product_id)
    await callback.message.answer("Mahsulot o'chirildi!")
    await callback.answer()

@router.callback_query(F.data == "edit_product")
async def edit_product_callback(callback: CallbackQuery, state: FSMContext):
    products = get_products()
    if products:
        await callback.message.answer("O'zgartirish uchun mahsulotni tanlang:",
                                     reply_markup=get_products_keyboard(products, "edit_prod"))
    else:
        await callback.message.answer("Hozircha mahsulotlar mavjud emas.")
    await callback.answer()

@router.callback_query(F.data.startswith("edit_prod_"))
async def process_edit_product(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split("_")[2])
    await state.update_data(product_id=product_id)
    await callback.message.answer("Yangi mahsulot nomini kiriting:")
    await state.set_state(Product.waiting_for_new_name)
    await callback.answer()

@router.message(Product.waiting_for_new_name)
async def process_new_product_name(message: Message, state: FSMContext):
    await state.update_data(new_name=message.text)
    categories = get_categories()
    await message.answer("Yangi kategoriyani tanlang:",
                         reply_markup=get_categories_keyboard(categories, "new_cat"))
    await state.set_state(Product.waiting_for_new_category)

@router.callback_query(F.data.startswith("new_cat_"))
async def process_new_category_selection(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split("_")[2])
    await state.update_data(new_category_id=category_id)
    await callback.message.answer("Yangi mahsulot narxini kiriting:")
    await state.set_state(Product.waiting_for_new_price)
    await callback.answer()

@router.message(Product.waiting_for_new_price)
async def process_new_product_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(new_price=price)
        await message.answer("Yangi mahsulot tavsifini kiriting:")
        await state.set_state(Product.waiting_for_new_description)
    except ValueError:
        await message.answer("Iltimos, to'g'ri narx kiriting (masalan, 100.50):")

@router.message(Product.waiting_for_new_description)
async def process_new_product_description(message: Message, state: FSMContext):
    user_data = await state.get_data()
    update_product(
        user_data['product_id'],
        user_data['new_name'],
        user_data['new_category_id'],
        user_data['new_price'],
        message.text
    )
    await message.answer("Mahsulot o'zgartirildi!")
    await state.clear()

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
    await state.set_state(Product.waiting_for_query)
    await callback.answer()