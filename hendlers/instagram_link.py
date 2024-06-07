from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType
from keyboards.default.default_keyboards import button
from load import dp, db
import re


class AddMoviesState(StatesGroup):
    waiting_for_kino_id = State()
    waiting_for_instagram_link = State()


@dp.message_handler(text="Instagram")
async def get_instagram(message: types.Message):
    instagram = db.get_instagram_link()
    if instagram:
        for movie in instagram:
            if len(movie) >= 9:
                text = f"""
ID: 🆔 {movie[0]}
Nomi: 🎥 {movie[1]}
Til: 🌐 {movie[2]}
Format: 📀 {movie[3]}
Janr: 🎭 {movie[4]}
Instagram: {movie[6]}
"""
                await message.answer(text=text)

        text = "Kino ID sini kiriting: "
        await AddMoviesState.waiting_for_kino_id.set()
        await message.answer(text=text)
    else:
        text = "Bo'sh tabillar mavjud emas"
        await message.answer(text=text)


@dp.message_handler(state=AddMoviesState.waiting_for_kino_id, content_types=ContentType.TEXT)
async def handle_kino_id(message: types.Message, state: FSMContext):
    kino_id = message.text
    if kino_id.isdigit():
        await state.update_data(kino_id=kino_id)
        await AddMoviesState.waiting_for_instagram_link.set()
        await message.answer("Instagram linkni kiriting: ")
    else:
        await message.answer("Iltimos, faqat raqam yuboring. Kino ID ni jo'nating.")


@dp.message_handler(state=AddMoviesState.waiting_for_instagram_link, content_types=ContentType.TEXT)
async def handle_instagram_link(message: types.Message, state: FSMContext):
    url = message.text
    match = re.search(r'/reel/([^/?]+)', url)
    if match:
        instagram_id = match.group(1)
        data = await state.get_data()
        kino_id = data.get('kino_id')
        print(instagram_id)
        print(kino_id)

        # Add the Instagram link to the database
        db.add_instagram_link(link=instagram_id, kino_id=kino_id)

        await state.finish()
        await message.answer("Instagram link muvaffaqiyatli qo'shildi.")
    else:
        await message.answer("Noto'g'ri Instagram link. Iltimos, qayta kiriting.")

