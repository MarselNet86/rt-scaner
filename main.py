from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.parser import check_data
from aiogram import Bot, Dispatcher, executor
from app import database as db
from config import token
import asyncio
import os

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    await db.db_start()
    print('Бот успешно запущен!')
    asyncio.create_task(periodic_check())


async def periodic_check():
    while True:
        await asyncio.sleep(5)
        file_path = check_data()
        if file_path:
            user_ids = await db.mailing()
            for user_id in user_ids:
                with open(file_path, 'rb') as file:
                    await bot.send_document(chat_id=user_id[0], document=file, caption="❗Пришли новые данные")

                try:
                    if os.path.isfile(path):
                        os.remove(path)
                    else:
                        print('Path is not a file')
                except Exception as e:
                    print(f"An error occurred while deleting the file: {e}")

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)