from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType
from keyboards.default.default_keyboards import button
from load import dp, db
import re


class AddMoviesStateYoutube(StatesGroup):
    waiting_for_kino_id_youtube = State()
    waiting_for_youtube_link = State()


@dp.message_handler(text="YouTube", state='*')
async def get_youtube(message: types.Message):
    youtube = db.get_youtube_link()
    if youtube:
        for movie in youtube:

            text = f"""
ID: 🆔 {movie[0]}
Nomi: 🎥 {movie[1]}
Youtube: 🔗 {movie[2]}
"""
            await message.answer(text=text)

        text = "Kino ID sini kiriting: "
        await AddMoviesStateYoutube.waiting_for_kino_id_youtube.set()
        await message.answer(text=text)
    else:
        text = "Kinolar mavjud emas"
        await message.answer(text=text)


@dp.message_handler(state=AddMoviesStateYoutube.waiting_for_kino_id_youtube, content_types=ContentType.TEXT)
async def handle_youtube_kino_id(message: types.Message, state: FSMContext):
    kino_id = message.text
    if kino_id.isdigit():
        await state.update_data(kino_id=kino_id)
        await AddMoviesStateYoutube.waiting_for_youtube_link.set()
        await message.answer("Youtube linkni kiriting: ")
    else:
        await message.answer("Iltimos, faqat raqam yuboring. Kino ID ni jo'nating.")


@dp.message_handler(state=AddMoviesStateYoutube.waiting_for_youtube_link, content_types=ContentType.TEXT)
async def handle_youtube_link(message: types.Message, state: FSMContext):
    url = message.text
    match = re.search(r'/shorts/([^/?]+)', url)
    if match:
        youtube_id = match.group(1)
        data = await state.get_data()
        kino_id = data.get('kino_id')
        # Add the Instagram link to the database
        db.add_youtube_link(link=youtube_id, kino_id=kino_id)

        await state.finish()
        await message.answer("Youtube link muvaffaqiyatli qo'shildi.")
    else:
        await message.answer("Noto'g'ri Youtube link. Iltimos, qayta kiriting.")
