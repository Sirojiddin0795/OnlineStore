from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from db.database import get_user, add_user

router = Router()

class Register(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    if user:
        await message.answer(f"Xush kelibsiz, {user[1]}! /menu orqali boshqaruv paneliga o'ting.")
    else:
        await message.answer("Iltimos, ro'yxatdan o'tish uchun ismingizni kiriting:")
        await state.set_state(Register.waiting_for_name)

@router.message(Register.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Telefon raqamingizni kiriting (masalan, +998901234567):")
    await state.set_state(Register.waiting_for_phone)

@router.message(Register.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    user_data = await state.get_data()
    add_user(message.from_user.id, user_data['name'], message.text)
    await message.answer("Ro'yxatdan o'tdingiz! /menu orqali boshqaruv paneliga o'ting.")
    await state.clear()