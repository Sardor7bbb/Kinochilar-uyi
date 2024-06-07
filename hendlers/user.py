from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType
from keyboards.default.default_keyboards import button
from load import dp, db
import re


#@dp.message_handler(text="")
#async def get_instagram(message: types.Message):
@dp.message_handler(content_types=ContentType.TEXT, state="waiting_for_instagram_link")
async def get_instagram(message: types.Message, state: FSMContext):
    text = message.text.strip()
    match = re.search(r'/reel/([^/?]+)', text)
    print(match)
    if match:
        instagram_id = match.group(1)
        if db.check_instagram_link(instagram_id):
            # Instagram link mavjud
            # Bazadan ma'lumotlarni olish
            movie = db.get_movie_by_instagram_id(instagram_id)
            print(movie)
            if movie:
                text = f"""
                ID: {movie[0]}
                Nomi: {movie[1]}
                Til: {movie[2]}
                Format: {movie[3]}
                Janr: {movie[4]}
                Instagram: {movie[6]}
                """
                await message.answer(text=text)
            else:
                text = "Bazada bunday ma'lumot topilmadi."
                await message.answer(text=text)
        else:
            # Instagram link mavjud emas
            text = "Bunday Instagram linki bazada topilmadi."
            await message.answer(text=text)
    else:
        # Tushirilgan matnda Instagram linki yo'q
        text = "Siz tushirgan matnda Instagram linki topilmadi."
        await message.answer(text=text)