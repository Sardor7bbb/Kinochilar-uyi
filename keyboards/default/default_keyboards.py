
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Rasimlar"),
            KeyboardButton(text="Rasim Joylash"),
        ],
        [
            KeyboardButton(text="Search 🔍"),
            KeyboardButton(text="Admin "),
        ],
        [
            KeyboardButton(text="Menyu")
        ],
        [
            KeyboardButton(text="Setting ⚙️")
        ]
    ], resize_keyboard=True
)