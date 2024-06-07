from aiogram import types
from utils.database_db import get_instagram_link
from load import dp


@dp.message_handler(func=lambda message: message.text.lower() == 'instagram')
async def process_instagram_link(message: types.Message):
    instagram = get_instagram_link
    # Ask user to enter Instagram link
    await message.answer("Iltimos, Instagram havolasini kiriting:")

    # Handle user's reply containing Instagram link
    async def handle_instagram_link(message: types.Message):
        # Check if the message contains a valid Instagram link
        instagram_link = message.text.strip()

        # Extracting the desired portion from the link
        try:
            start_index = instagram_link.find('/reel/') + len('/reel/')
            end_index = instagram_link.find('/?', start_index)
            portion = instagram_link[start_index:end_index]
        except ValueError:
            portion = "Noto'g'ri havola formati"

        # Send back the extracted portion to the user
        await message.answer(f"Instagram havolasining C7138HHN9o4 qismini olib chiqdim: {portion}")

    # Register a new message handler specifically for handling Instagram link
    dp.register_message_handler(handle_instagram_link, content_types=types.ContentTypes.TEXT)