from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from db.database import add_category, get_categories, delete_category, update_category, get_user
from keyboards.inline import get_categories_keyboard

router = Router()

class Category(StatesGroup):
    waiting_for_name = State()
    waiting_for_new_name = State()

@router.message(Command("add_category"))
async def add_category_command(message: Message, state: FSMContext):
    if not get_user(message.from_user.id):
        return await message.reply("❌ Ro‘yxatdan o‘tmagansiz.")
    await message.answer("Yangi kategoriya nomini kiriting:")
    await state.set_state(Category.waiting_for_name)

@router.message(Category.waiting_for_name)
async def process_category_name(message: Message, state: FSMContext):
    if add_category(message.text):
        await message.answer(f"Kategoriya '{message.text}' qo'shildi!")
    else:
        await message.answer("Bu nomdagi kategoriya allaqachon mavjud!")
    await state.clear()

@router.callback_query(F.data == "add_category")
async def add_category_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Yangi kategoriya nomini kiriting:")
    await state.set_state(Category.waiting_for_name)
    await callback.answer()

@router.callback_query(F.data == "delete_category")
async def delete_category_callback(callback: CallbackQuery):
    categories = get_categories()
    if categories:
        await callback.message.answer("O'chirish uchun kategoriyani tanlang:",
                                     reply_markup=get_categories_keyboard(categories, "del_cat"))
    else:
        await callback.message.answer("Hozircha kategoriyalar mavjud emas.")
    await callback.answer()

@router.callback_query(F.data.startswith("del_cat_"))
async def process_delete_category(callback: CallbackQuery):
    category_id = int(callback.data.split("_")[2])
    delete_category(category_id)
    await callback.message.answer("Kategoriya o'chirildi!")
    await callback.answer()

@router.callback_query(F.data == "edit_category")
async def edit_category_callback(callback: CallbackQuery, state: FSMContext):
    categories = get_categories()
    if categories:
        await callback.message.answer("O'zgartirish uchun kategoriyani tanlang:",
                                     reply_markup=get_categories_keyboard(categories, "edit_cat"))
    else:
        await callback.message.answer("Hozircha kategoriyalar mavjud emas.")
    await callback.answer()

@router.callback_query(F.data.startswith("edit_cat_"))
async def process_edit_category(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split("_")[2])
    await state.update_data(category_id=category_id)
    await callback.message.answer("Yangi kategoriya nomini kiriting:")
    await state.set_state(Category.waiting_for_new_name)
    await callback.answer()

@router.message(Category.waiting_for_new_name)
async def process_new_category_name(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if update_category(user_data['category_id'], message.text):
        await message.answer("Kategoriya nomi o'zgartirildi!")
    else:
        await message.answer("Bu nomdagi kategoriya allaqachon mavjud!")
    await state.clear()