
from load import dp, db
from aiogram import executor, Dispatcher


async def on_startup(dispatcher):
    db.create_table()


async def on_shutdown(dispatcher):
    db.connect.close()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
