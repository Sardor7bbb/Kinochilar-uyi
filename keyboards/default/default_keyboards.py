
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Kinolar  🎦"),
            KeyboardButton(text="Kino qo'shish  🎬"),
        ],
        [
            KeyboardButton(text="Instagram"),
            KeyboardButton(text="YouTube"),
        ],
        [
            KeyboardButton(text="Menyu")
        ],
        [
            KeyboardButton(text="Setting ⚙️")
        ]
    ], resize_keyboard=True
)
