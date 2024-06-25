from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType, InputMediaVideo

from keyboards.default.default_keyboards import button
from load import dp, db
from main.config import ADMIN
from status.movies import AddMoviesState
import re

INSTAGRAM_REGEX = r"(https?://)?(www\.)?(instagram\.com\.am)/[A-Za-z0-9-_]+"
YOUTUBE_SHORTS_REGEX = r"(https?://)?(www\.)?(youtube\.com)/([A-Za-z0-9-_]+)(\?.*)?"
YOUTUBE_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/([A-Za-z0-9-_]+)(\?.*)?"


@dp.message_handler(commands='start', state='*')
async def start(message: types.Message, state: FSMContext):

    if db.get_user_chat_id(chat_id=message.chat.id):
        if message.from_user.id == int(ADMIN):
            text = "Assalomu Alekum 👋"
            await message.answer(text=text, reply_markup=button)
        else:
            text = """
Assalomu Alekum 👋 
Instagram yoki Youtube linkini jo'nating"""
            await state.set_state('get-link')
            await message.answer(text=text)
    else:
        text = """
Assalomu Alekum 👋 
Instagram yoki Youtube linkini jo'nating"""
        user_id = message.chat.id
        db.get_new_user_id(user_id=user_id)
        await state.set_state('get-link')
        await message.answer(text=text)


@dp.message_handler(state='get-link')
async def get_link_handler(message: types.Message, state: FSMContext):
    link = message.text
    if re.search(INSTAGRAM_REGEX, link):
        # Instagram

        match = re.search(r'/reel/([^/?]+)', link)
        if match:
            instagram_link = match.group(1)
            search_link = db.search_movies_instagram(link=instagram_link)
            if search_link:
                movie_id = search_link[0]
                user_id = db.get_user_chat_id(chat_id=message.chat.id)
                user_download = db.get_user_downloads(user_id=user_id[0][0], movie_id=movie_id)
                if user_download is None:
                    db.user_downloader(user_id=user_id[0][0], movie_id=movie_id)

                for movie in [search_link]:
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

    elif re.search(YOUTUBE_SHORTS_REGEX, link):
        # Youtube

        match = re.search(r'/shorts/([^?]+)', link)
        if match:
            youtube_link = match.group(1)
            search_link = db.search_movies_youtube(link=youtube_link)
            if search_link:
                movie_id = search_link[0]
                user_id = db.get_user_chat_id(chat_id=message.chat.id)
                user_download = db.get_user_downloads(user_id=user_id[0][0], movie_id=movie_id)
                if user_download is None:
                    db.user_downloader(user_id=user_id[0][0], movie_id=movie_id)

                for movie in [search_link]:
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

    elif re.search(YOUTUBE_REGEX, link):
        # Youtube

        match = re.search(r'/youtu.be/([^?]+)', link)
        print('nima')
        print(match)
        if match:
            youtube_link = match.group(1)
            search_link = db.search_movies_youtube(link=youtube_link)
            if search_link:
                movie_id = search_link[0]
                user_id = db.get_user_chat_id(chat_id=message.chat.id)
                user_download = db.get_user_downloads(user_id=user_id[0][0], movie_id=movie_id)
                if user_download is None:
                    db.user_downloader(user_id=user_id[0][0], movie_id=movie_id)

                for movie in [search_link]:
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

    else:
        text = "Instaram va Youtube linkini jo'nating!"
        await message.answer(text=text)


@dp.message_handler(text='')
async def users_coments(message: types.Message, state: FSMContext):
    text = 'Salom Qanday yordam bera olaman'
    await message.answer(text=text)
