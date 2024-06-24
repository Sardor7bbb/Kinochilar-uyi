from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaVideo

from load import dp, db


@dp.message_handler(text="Kinolar  🎦", state='*')
async def get_random_foto(message: types.Message, state: FSMContext):
    movies = db.movies()
    print(movies)
    if movies:
        for movie in movies:
            # Video file ID
            video_file_id = movie[5]

            # Caption (video matni)
            caption = f"""
ID: 🆔 {movie[0]}
Nomi: 🎥 {movie[1]}
Til: 🌐 {movie[2]}
Format: 📀 {movie[3]}
Janr: 🎭 {movie[4]}
Instagram: 🔗 {movie[6]}
Youtube: 🔗 {movie[7]}
"""

            # Video va caption bir xabar ichida yuborish
            media = InputMediaVideo(media=video_file_id, caption=caption)
            await message.answer_media_group([media])




