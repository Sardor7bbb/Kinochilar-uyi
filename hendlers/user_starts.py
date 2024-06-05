from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import message, KeyboardButton, ReplyKeyboardMarkup

from keyboards.default.default_keyboards import button
from load import dp, db
from main.config import ADMIN


@dp.massage_handler(commands=['start'])
async def start(message: types.Message):
    text = "Assalomu Alekum 👋"
    user_id = message.from_user.id
    print("Nima gap")
    print(user_id)
    await message.answer(text=text)
