
from aiogram.dispatcher.filters.state import State, StatesGroup


class AddMoviesState(StatesGroup):
    movie_name = State()
    language = State()
    quality = State()
    genre = State()
    categories = State()
    movie_id = State()
