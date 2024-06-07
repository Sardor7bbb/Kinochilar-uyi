from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from keyboards.default.default_keyboards import button
from load import dp, db
from status.movies import AddMoviesState


@dp.message_handler(text="Kino qo'shish  🎬")
async def get_movies(message: types.Message):
    text = "Kino nomini kiriting: "
    await message.answer(text=text)
    await AddMoviesState.movie_name.set()


@dp.message_handler(state=AddMoviesState.movie_name)
async def get_movie_name(message: types.Message, state: FSMContext):
    await state.update_data(movie_name=message.text, id=message.chat.id)
    text = "Tilni kiriting: "
    await message.answer(text=text)
    await AddMoviesState.language.set()


@dp.message_handler(state=AddMoviesState.language)
async def get_language(message: types.Message, state: FSMContext):
    await state.update_data(language=message.text)
    text = "Video sifatini kiriting: "
    await message.answer(text=text)
    await AddMoviesState.quality.set()


@dp.message_handler(state=AddMoviesState.quality)
async def get_quality(message: types.Message, state: FSMContext):
    await state.update_data(quality=message.text)
    text = "Film janrini kiriting: "
    await message.answer(text=text)
    await AddMoviesState.genre.set()


@dp.message_handler(state=AddMoviesState.genre)
async def get_genre(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)
    text = "Yosh chegarasini kiriting: "
    await message.answer(text=text)
    await AddMoviesState.categories.set()


@dp.message_handler(state=AddMoviesState.categories)
async def get_categories(message: types.Message, state: FSMContext):
    await state.update_data(categories=message.text)
    text = "Filimni yuklang: "
    await message.answer(text=text)
    await AddMoviesState.movie_id.set()


@dp.message_handler(content_types=ContentType.VIDEO, state=AddMoviesState.movie_id)
async def get_movie_id(message: types.Message, state: FSMContext):
    video_file_id = message.video.file_id
    await state.update_data(movie_id=video_file_id)
    data = await state.get_data()
    print(data)
    if db.get_add_movies(data):
        text = "Successfully deploy ✅"
        await message.answer(text=text, reply_markup=button)
    else:
        text = "Bot problems 🛠"
        await message.answer(text=text)
    await state.finish()
