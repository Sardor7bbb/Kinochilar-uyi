from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType, InputMediaVideo

from keyboards.default.default_keyboards import button
from load import dp, db
from main.config import ADMIN
from status.movies import AddMoviesState
import re


@dp.message_handler(commands='start')
async def start(message: types.Message, state: FSMContext):

    if db.get_user_chat_id(chat_id=message.chat.id):
        if message.from_user.id == int(ADMIN):
            text = "Assalomu Alekum 👋"
            await message.answer(text=text, reply_markup=button)
        else:
            text = 'Linkni jonating'
            await state.set_state('get-link')
            await message.answer(text=text)
    else:
        text = 'Linkni jonating'
        user_id = message.chat.id
        db.get_new_user_id(user_id=user_id)
        await state.set_state('get-link')
        await message.answer(text=text)


@dp.message_handler(state='get-link')
async def get_link_handler(message: types.Message, state: FSMContext):
    link = message.text
    match = re.search(r'/reel/([^/?]+)', link)
    if match:
        instagram_link = match.group(1)
        search_link = db.search_movies(link=instagram_link)
        if search_link:

            for movie in [search_link]:
                print(movie)
                video_file_id = movie[5]

                # Caption (video matni)
                caption = f"""
Nomi: 🎥 {movie[1]}
Til: 🌐 {movie[2]}
Format: 📀 {movie[3]}
Janr: 🎭 {movie[4]}
"""
                # Video va caption bir xabar ichida yuborish
                media = InputMediaVideo(media=video_file_id, caption=caption)
                await message.answer_media_group([media])

        else:
            text = "Bunday film mavjud emas"
            await message.answer(text=text)

    else:
        text = "Noto'g'ri link format. Iltimos, qayta urinib ko'ring."
        await message.answer(text=text)

