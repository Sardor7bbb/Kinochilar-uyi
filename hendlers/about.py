from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaVideo

from load import dp, db


@dp.message_handler(text="About", state='*')
async def get_admin_about(message: types.Message, state: FSMContext):
    text = f"""
Foydalanuvchilar soni: {db.get_user_about()[0]}
Kinolar soni: {db.get_movies_about()[0]}
Yuklab olishlar soni: 
Id: {db.get_download_about()[0]}  
Movie name: {db.get_download_about()[1]}  
Number of downloads: {db.get_download_about()[2]}
    """
    print(text)
    await message.answer(text=text)
