from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaVideo

from load import dp, db


@dp.message_handler(text="About")
async def get_random_foto(message: types.Message, state: FSMContext):
    about = db.get_about()
    print(about)
